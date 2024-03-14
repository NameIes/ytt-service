"""That module contains utility functions for working with messages"""

import json
from soc_telegram.models import MediaGroup, ChannelOfCoordination, MediaGroupItem
from soc_telegram.utils.telegram_api import send_message, delete_message
from soc_telegram.utils.providers import send_media_group_to_telegram_chat, \
    send_message_to_telegram_chat


def remove_join_message(message: dict) -> None:
    # TODO: Remove join message
    print('\n\nTODO: Remove join message\n\n')


def is_media_group(message_id: str, chat_id: str) -> bool:
    return MediaGroup.objects.filter(
        first_message_id=message_id,
        from_chat_id=chat_id
    ).exists()


def copy_media_group(chat_id: str, to_main_channels: bool = False, message_id: str = None, mg_id: int = None) -> int | None:
    cofc = ChannelOfCoordination.objects.get(chat_id=chat_id)
    if message_id:
        media_group = MediaGroup.objects.get(
            first_message_id=message_id,
            from_chat_id=chat_id
        )
    else:
        media_group = MediaGroup.objects.get(id=mg_id)

    if to_main_channels:
        for channel in cofc.business.channels.all():
            if channel.is_calc_channel:
                continue
            send_media_group_to_telegram_chat(channel, media_group=media_group)

        # TODO: Send media group to VK
    else:
        return send_media_group_to_telegram_chat(cofc, media_group=media_group)


def copy_message(message_id: str, chat_id: str, to_main_channels: bool = False) -> str | None:
    cofc = ChannelOfCoordination.objects.get(chat_id=chat_id)
    if to_main_channels:
        for channel in cofc.business.channels.all():
            if channel.is_calc_channel:
                continue
            send_message_to_telegram_chat(channel, message_id, chat_id)

        # TODO: Send message to VK
    else:
        return send_message_to_telegram_chat(cofc, message_id, chat_id)


def send_approve_keyboard(message: dict, is_media_group: bool, mg_id: int | str) -> None:
    keyboard_post = {
        'chat_id': message['message_reaction']['chat']['id'],
        'text': 'Подтвердить публикацию?',
        'reply_markup': {
            'inline_keyboard': [
                [{'text': 'Опубликовать ✅', 'callback_data': json.dumps({
                    'type': 'media_group' if is_media_group else 'message',
                    'success': True,
                    'mg_id': mg_id
                })}],
                [{'text': 'Отменить публикацию ❌', 'callback_data': json.dumps({
                    'type': 'media_group' if is_media_group else 'message',
                    'success': False,
                    'mg_id': mg_id
                })}]
            ],
            'resize_keyboard': True
        }
    }

    send_message(keyboard_post)


def delete_approve_keyboard(message: dict) -> None:
    data = {
        'chat_id': message['callback_query']['message']['chat']['id'],
        'message_id': message['callback_query']['message']['message_id']
    }

    delete_message(data)


def _get_or_create_media_group(mg_id, from_chat, first_message_id=None):
    """
    Get or create a media group object based on the provided media group ID and from_chat ID.
    Optionally, the first_message_id can also be provided.
    Returns the media group object.
    """
    try:
        mg_obj = MediaGroup.objects.get(media_group_id=mg_id, from_chat_id=from_chat)
    except MediaGroup.DoesNotExist:
        mg_obj = MediaGroup.objects.create(
            media_group_id=mg_id, from_chat_id=from_chat, first_message_id=first_message_id
        )
    return mg_obj


def _get_media_type(message: dict) -> str:
    """
    Function that takes a message dictionary and returns the media type if present.

    Args:
        message (dict): The message dictionary containing the media types.

    Returns:
        str: The media type if present, otherwise None.
    """
    for m_type in ('audio', 'video', 'document', 'photo', 'animation'):
        if message['message'].get(m_type, None) is not None:
            return m_type
    return None


def collect_media_group(message: dict) -> None:
    mg_id = None
    try:
        mg_id = message['message']['media_group_id']
    except KeyError:
        return

    if mg_id is None:
        return

    if not ChannelOfCoordination.objects.filter(
        chat_id=message['message']['chat']['id']
        ).exists():
        return

    mg_obj = _get_or_create_media_group(
        mg_id=mg_id,
        from_chat=message['message']['chat']['id'],
        first_message_id=message['message']['message_id']
    )

    m_type = _get_media_type(message)
    file = MediaGroupItem(
        media_group=mg_obj,
        media_type=m_type,
        file_id=message['message'][m_type][-1]['file_id'],
        message_id=message['message']['message_id']
    )
    try:
        file.caption = message['message']['caption']
    except KeyError:
        pass
    file.save()
