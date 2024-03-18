from soc_telegram.models import Channel, MediaGroup, ChannelOfCoordination
from soc_telegram.utils.telegram_api import send_media_group, copy_message


def send_media_group_to_telegram_chat(
    channel: Channel | ChannelOfCoordination,
    media_group: MediaGroup = None
    ) -> int:

    data = {
        'chat_id': channel.chat_id,
        'media': media_group.serialize_for_send(),
    }

    try:
        if channel.thread_id:
            data['message_thread_id'] = channel.thread_id
    except AttributeError:
        pass

    send_media_group(data)

    return media_group.id


def send_message_to_telegram_chat(
    channel: Channel | ChannelOfCoordination,
    message_id: str,
    chat_id: str
    ) -> str:
    data = {
        'chat_id': channel.chat_id,
        'from_chat_id': chat_id,
        'message_id': message_id,
    }

    try:
        if channel.thread_id:
            data['message_thread_id'] = channel.thread_id
    except AttributeError:
        pass

    copy_message(data)

    return data['message_id']
