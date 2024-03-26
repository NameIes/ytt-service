from vk_api import VkUpload
from django.conf import settings
from soc_telegram.utils.files import save_files_from_telegram


def wall_post(groups, urls, texts):
    if len(groups) == 0:
        return

    if len(urls) == 0 and len(texts) == 0:
        return

    if len(texts) == 0:
        text = None
    else:
        text = texts[0]

    files = save_files_from_telegram(urls)

    for group in groups:
        attachments = []
        for file in files:
            upload = VkUpload(settings.VK_SESSION)
            if file.filetype == 'photo':
                response = upload.photo_wall(
                    file.file.path,
                    group_id=group.group_id,
                )

                attachments.append('photo{}_{}'.format(
                    response[0]['owner_id'],
                    response[0]['id'],
                ))

            if file.filetype == 'video':
                response = upload.video(
                    file.file.path,
                    group_id=group.group_id
                )

                attachments.append('video{}_{}'.format(
                    response['owner_id'],
                    response['video_id'],
                ))

            if file.filetype == 'document':
                response = upload.document_wall(
                    file.file.path,
                    group_id=group.group_id,
                    title=file.file.name
                )

                attachments.append('doc{}_{}'.format(
                    response['doc']['owner_id'],
                    response['doc']['id'],
                ))

        wall_post_kwargs = {
            'owner_id': -int(group.group_id),
            'from_group': 1,
        }
        if text:
            wall_post_kwargs['message'] = text
        if len(attachments) > 0:
            wall_post_kwargs['attachments'] = ','.join(attachments)
        settings.VK_SESSION.wall.post(**wall_post_kwargs)
