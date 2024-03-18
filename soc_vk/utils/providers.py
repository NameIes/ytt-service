from soc_vk.models import Group
from soc_telegram.models import MediaGroup
from soc_telegram.utils.telegram_api import forward_message, get_file
from soc_telegram.utils.files import save_files_from_telegram
from django.conf import settings
from vk_api.upload import VkUpload


def _upload_file_to_vk(uploader: VkUpload, file, group: Group) -> dict:
    IMAGE = ('.ras', '.xwd', '.bmp', '.jpe', '.jpg', '.jpeg', '.xpm', '.ief', '.pbm', '.tif', '.gif', '.ppm', '.xbm', '.tiff', '.rgb', '.pgm', '.png', '.pnm')
    AUDIO = ('.ra', '.aif', '.aiff', '.aifc', '.wav', '.au', '.snd', '.mp3', '.mp2')
    VIDEO = ('.m1v', '.mpeg', '.mov', '.qt', '.mpa', '.mpg', '.mpe', '.avi', '.movie', '.mp4')

    extension = file.get_extension()

    result = {
        'type': ''
    }

    if extension in IMAGE:
        result['type'] = 'photo'
        result['result'] = uploader.photo_wall(file.file.path, group_id=group.group_id)
        return result
    if extension in AUDIO:
        result['type'] = 'audio'
        result['result'] = uploader.audio_message(file.file.path, group_id=group.group_id)
        return result
    if extension in VIDEO:
        result['type'] = 'video'
        result['result'] = uploader.video(file.file.path, wallpost=False, group_id=group.group_id)
        return result

    result['type'] = 'doc'
    result['result'] = uploader.document_wall(file.file.path, group_id=group.group_id)
    return result


def send_media_group_to_vk_group(group: Group, media_group: MediaGroup) -> None:
    download_url = f'https://api.telegram.org/file/bot{settings.TELEGRAM_BOT_TOKEN}/'
    files_urls = [get_file({'file_id': item.file_id}) for item in media_group.items.all()]
    files_urls = [download_url + i['result']['file_path'] for i in files_urls]

    first_item = media_group.items.first()
    caption = first_item.caption if first_item.caption else None
    downloaded_files = save_files_from_telegram(files_urls)

    uploader = VkUpload(settings.VK_SESSION)
    uploaded_files = [_upload_file_to_vk(uploader, file, group) for file in downloaded_files]

    attachments = []
    for file in uploaded_files:
        attachments.append('{filetype}{owner_id}_{media_id}'.format(
            filetype=file['type'],
            owner_id=file['result'][0]['owner_id'],
            media_id=file['result'][0]['id']
        ))
    attachments = ','.join(attachments)

    settings.VK_SESSION.wall.post(
        owner_id=int(group.group_id) * -1,
        from_group=1,
        message=caption,
        attachments=attachments
    )


def send_message_to_vk_group(group: Group, message_id: str, chat_id: str) -> None:
    # -1001642814889
    pass
