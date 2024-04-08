from vk_api import VkUpload
from django.conf import settings
from soc_telegram.utils.files import save_files_from_telegram
from websites.utils.providers import copy_post_to_websites


def wall_post(groups, urls, texts):
    """
    Данный метод загружает файлы из Telegram на сервер и отправляет пост в группу ВК.
    """
    if len(groups) == 0:
        return

    if len(urls) == 0 and len(texts) == 0:
        return

    if len(texts) == 0:
        text = None
    else:
        text = None
        for text_ in texts:
            if text_ is not None:
                text = text_
                break

    files = save_files_from_telegram(urls)
    images = []
    videos = []

    for group in groups:
        attachments = []
        for file in files:
            upload = VkUpload(settings.VK_SESSION)
            if file.filetype == 'photo':
                response = upload.photo_wall(
                    file.file.path,
                    group_id=group.group_id,
                )

                images.append(file)

                attachments.append('photo{}_{}'.format(
                    response[0]['owner_id'],
                    response[0]['id'],
                ))

            if file.filetype == 'video':
                response = upload.video(
                    file.file.path,
                    group_id=group.group_id
                )

                videos.append({
                    'owner_id': '-' + str(response['owner_id']),
                    'video_id': response['video_id'],
                })

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
            wall_post_kwargs['message'] = text.encode('utf-8')
        if len(attachments) > 0:
            wall_post_kwargs['attachments'] = ','.join(attachments)
        settings.VK_SESSION.wall.post(**wall_post_kwargs)

    business = groups[0].business

    copy_post_to_websites(business, images, videos, text)
