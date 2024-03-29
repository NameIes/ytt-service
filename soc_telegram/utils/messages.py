"""That module contains utility functions for working with messages"""

import json
import threading
from django.conf import settings
from soc_telegram.models import ChannelOfCoordination, Message
from soc_telegram.utils.telegram_api import send_message, delete_message, copy_messages
from soc_vk.utils.providers import wall_post


def remove_join_message(message: dict) -> None:
    """
    Данный метод удаляет сообщение о присоединении к каналу.
    """
    data = {
        'chat_id': message['message']['chat']['id'],
        'message_id': message['message']['message_id']
    }

    delete_message(data)


def copy_message(message_id, to_main_channels, from_channel=None):
    """
    Данный метод копирует сообщение из канала согласований.
    Если to_main_channels = True, то копируются в основные каналы Telegram, и группы ВК.
    Иначе копирует в канал согласований.
    """

    # Получаем канал согласований, бизнес, и само сообщение
    try:
        cofc = ChannelOfCoordination.objects.get(
            chat_id=from_channel
        )
        message_obj = cofc.messages.get(
            tg_message_id=message_id,
        )
    except Message.DoesNotExist:
        raise Exception('Message does not exist')

    business = message_obj.coordination_channel.business

    # Определяем является ли сообщение группой сообщений
    # В любом случае в итоге получится список сообщений (даже если сообщение одно)
    try:
        media_group_id = message_obj.message['message']['media_group_id']
        messages_objects = cofc.messages.filter(
            message__message__media_group_id=media_group_id
        )
    except KeyError:
        messages_objects = cofc.messages.filter(
            tg_message_id=message_id
        )

    # Преобразуем все сообщения в список из message_id
    messages_ids = list(
        messages_objects.values_list('tg_message_id', flat=True)
    )

    # Определяем куда копировать пост (в основные каналы/в канал согласований)
    # В любом случае получится список каналов (даже если канал один)
    target_chats = []
    if to_main_channels:
        target_chats = list(
            business.channels.exclude(is_calc_channel=True)
        )
    else:
        target_chats.append(message_obj.coordination_channel)

    # Отправляем пост в целевые каналы
    for chat in target_chats:
        data = {
            'chat_id': chat.chat_id,
            'from_chat_id': message_obj.coordination_channel.chat_id,
            'message_ids': messages_ids
        }
        if to_main_channels and chat.thread_id:
            data['message_thread_id'] = chat.thread_id

        copy_messages(data)

    # Проверяем есть ли необходимость отправлять пост в группы ВК
    if not to_main_channels:
        return

    if business.groups.count() == 0:
        return

    # Получаем ссылки на файлы и текст сообщения для поста в ВК
    urls = []
    texts = []
    for message in messages_objects:
        file_url = message.get_file_url()
        if file_url is not None:
            try:
                urls.append([
                    file_url[0],
                    f'https://api.telegram.org/file/bot{settings.TELEGRAM_BOT_TOKEN}/' + \
                    file_url[1]['result']['file_path']
                ])
            except KeyError:
                pass

        text = message.get_text()
        if text:
            texts.append(text)

    # Запускаем отдельный поток для загрузки файлов на сервер и поста в ВК
    thread = threading.Thread(
        target=wall_post,
        args=(business.groups.all(), urls, texts)
    )
    thread.start()


def send_approve_keyboard(target_chat_id, message_id, from_channel) -> None:
    """Данный метод отправляет клавиатуру с подтверждением публикации."""
    keyboard_post = {
        'chat_id': target_chat_id,
        'text': 'Подтвердить публикацию?',
        'reply_markup': {
            'inline_keyboard': [
                [{'text': 'Опубликовать ✅', 'callback_data': json.dumps({
                    'succ': True,
                    'mid': message_id,
                    'cid': from_channel
                })}],
                [{'text': 'Отменить публикацию ❌', 'callback_data': json.dumps({
                    'succ': False,
                    'mid': message_id,
                    'cid': from_channel
                })}]
            ],
            'resize_keyboard': True
        }
    }

    send_message(keyboard_post)


def delete_approve_keyboard(message: dict) -> None:
    """Данный метод удаляет клавиатуру с подтверждением публикации."""
    data = {
        'chat_id': message['callback_query']['message']['chat']['id'],
        'message_id': message['callback_query']['message']['message_id']
    }

    delete_message(data)


def collect_message(message: dict) -> None:
    """Данный метод сохраняет сообщение в БД."""
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
