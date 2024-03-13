"""That module contains utility functions for working with messages"""

import json
from soc_telegram.models import MediaGroup, ChannelOfCoordination
from soc_telegram.utils.telegram_api import send_message
from soc_telegram.utils.providers import send_media_group_to_telegram_chat, \
    send_message_to_telegram_chat


def remove_join_message(message: dict) -> None:
    # TODO: Remove join message
    print('\n\nTODO: Remove join message\n\n')


def is_media_group(message: dict) -> bool:
    return MediaGroup.objects.filter(
        first_message_id=message['message_reaction']['message_id'],
        from_chat_id=message['message_reaction']['chat']['id']
    ).exists()


def copy_media_group(message: dict, to_main_channels: bool = False) -> int | None:
    cofc = ChannelOfCoordination.objects.get(chat_id=message['message_reaction']['chat']['id'])
    media_group = MediaGroup.objects.get(
        first_message_id=message['message_reaction']['message_id'],
        from_chat_id=message['message_reaction']['chat']['id']
    )

    if to_main_channels:
        for channel in cofc.business.channels.all():
            send_media_group_to_telegram_chat(channel, media_group=media_group)

        # TODO: Send media group to VK
    else:
        return send_media_group_to_telegram_chat(cofc, media_group=media_group)


def copy_message(message: dict, to_main_channels: bool = False) -> str | None:
    cofc = ChannelOfCoordination.objects.get(chat_id=message['message_reaction']['chat']['id'])

    if to_main_channels:
        for channel in cofc.business.channels.all():
            send_message_to_telegram_chat(channel, message=message)

        # TODO: Send message to VK
    else:
        return send_message_to_telegram_chat(cofc, message=message)


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
