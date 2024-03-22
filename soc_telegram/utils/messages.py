"""That module contains utility functions for working with messages"""

import json
from soc_telegram.models import ChannelOfCoordination, Message
from soc_telegram.utils.telegram_api import send_message, delete_message, copy_messages


def remove_join_message(message: dict) -> None:
    data = {
        'chat_id': message['message']['chat']['id'],
        'message_id': message['message']['message_id']
    }

    delete_message(data)


def copy_message(message_id, to_main_channels, from_channel=None):
    try:
        message_obj = Message.objects.get(
            tg_message_id=message_id,
            message__message__chat__id=str(from_channel)
        )
    except Message.DoesNotExist:
        raise Exception('Message does not exist')

    business = message_obj.coordination_channel.business

    try:
        media_group_id = message_obj.message['message']['media_group_id']
        messages_objects = Message.objects.filter(
            message__message__media_group_id=media_group_id
        )
    except KeyError:
        messages_objects = Message.objects.filter(
            tg_message_id=message_id
        )

    messages_ids = list(
        messages_objects.values_list('tg_message_id', flat=True)
    )

    target_chats = []
    if to_main_channels:
        target_chats = list(
            business.channels.exclude(is_calc_channel=True)
        )
    else:
        target_chats.append(message_obj.coordination_channel)

    for chat in target_chats:
        data = {
            'chat_id': chat.chat_id,
            'from_chat_id': message_obj.coordination_channel.chat_id,
            'message_ids': messages_ids
        }
        if to_main_channels and chat.thread_id:
            data['message_thread_id'] = chat.thread_id

        copy_messages(data)


def send_approve_keyboard(target_chat_id, message_id, from_channel) -> None:
    keyboard_post = {
        'chat_id': target_chat_id,
        'text': 'Подтвердить публикацию?',
        'reply_markup': {
            'inline_keyboard': [
                [{'text': 'Опубликовать ✅', 'callback_data': json.dumps({
                    'success': True,
                    'message_id': message_id,
                    'from_channel': from_channel,
                })}],
                [{'text': 'Отменить публикацию ❌', 'callback_data': json.dumps({
                    'success': False,
                    'message_id': message_id,
                    'from_channel': from_channel,
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


def collect_message(message: dict) -> None:
    try:
        coordination_channel = ChannelOfCoordination.objects.filter(
            chat_id=message['message']['chat']['id']
        ).first()
    except KeyError:
        return

    if not coordination_channel:
        return

    message_obj = Message(
        coordination_channel=coordination_channel,
        message=message,
        tg_message_id=message['message']['message_id']
    )
    message_obj.save()
