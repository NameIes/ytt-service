"""That module contains services"""

import json
import requests

from core.settings import TELEGRAM_API_URL
from db_models.models import ContactPerson, Worker
from soc_telegram.models import Channel, MediaGroup


def get_current_contact_person(**model_param) -> ContactPerson | None:
    """
    **model_param: Поля модели по которой произойдет выборка объекта модели ContactPerson
    """
    try:
        contact_person = ContactPerson.objects.get(**model_param)
        return contact_person
    except ContactPerson.DoesNotExist:
        return None


def get_current_channel(**model_param) -> Channel | None:
    """
    **model_param: Поля модели по которой произойдет выборка объекта модели ContactPerson
    """
    try:
        channel = Channel.objects.get(**model_param)
        return channel
    except Channel.DoesNotExist:
        return None


def get_current_worker(**model_param) -> Worker | None:
    """
    **model_param: Поля модели по которой произойдет выборка объекта модели Worker
    """
    try:
        worker = Worker.objects.get(**model_param)
        return worker
    except Worker.DoesNotExist:
        return None


def get_data_for_copy(chat_id: str, target_chat_id: str, message_id: str) -> dict:
    """
    A function to generate data for copying a message to another chat.

    Args:
        chat_id (str): The ID of the source chat.
        target_chat_id (str): The ID of the target chat.
        message_id (str): The ID of the message to be copied.

    Returns:
        dict: A dictionary containing the necessary data for copying the message.
    """
    data = {
        'chat_id': target_chat_id,
        'from_chat_id': chat_id,
        'message_id': message_id,
    }
    thread_id = Channel.objects.get(chat_id=target_chat_id).thread_id
    if thread_id:
        data['message_thread_id'] = thread_id
    if chat_id == target_chat_id:
        data.update({'reply_markup': {
            'inline_keyboard': [
                [{'text': 'Опубликовать ✅', 'callback_data': 'success'}],
                [{'text': 'Отменить публикацию ❌', 'callback_data': 'failure'}]
            ],
            'resize_keyboard': True
        }})
    return data


def send_keyboard(for_mg, target_chat, msg_ids):
    """
    A function to send a keyboard message using Telegram API.

    Args:
        for_mg (MediaGroup): the message to be sent
        target_chat (dict): the chat to send the message to
        msg_ids (list): message IDs associated with the message

    Returns:
        None
    """
    method = 'sendMessage'
    url = TELEGRAM_API_URL + method
    data = {
        'text': 'Опубликовать данный пост?',
        'reply_markup': {
            'inline_keyboard': [
                [{'text': 'Опубликовать ✅', 'callback_data': json.dumps({
                    'success': True,
                    'mg_id': for_mg.id,
                    'msg_ids': msg_ids
                })}],
                [{'text': 'Отменить публикацию ❌', 'callback_data': json.dumps({
                    'success': False,
                    'mg_id': for_mg.id,
                    'msg_ids': msg_ids
                })}]
            ],
            'resize_keyboard': True
        }
    }
    requests.post(url, json={**target_chat, **data}, timeout=10)


def send_media_group(mg_obj, target_chat, send_kb=False):
    """
    Sends a media group to the specified target chat.

    Args:
        mg_obj (MediaGroup): The media group object to send.
        target_chat (dict): The target chat to send the media group to.
        send_kb (bool): A boolean indicating whether to send a keyboard
                        along with the media group (default is False).

    Returns:
        None
    """
    method = 'sendMediaGroup'
    url = TELEGRAM_API_URL + method
    response = requests.post(url, json=mg_obj.serialize_for_send(target_chat), timeout=10)

    response_data = response.json()
    msg_ids = []
    for msg in response_data['result']:
        msg_ids.append(msg['message_id'])

    if send_kb:
        chat_for_kb = {
            'chat_id': target_chat['chat_id']
        }
        try:
            chat_for_kb['message_thread_id'] = target_chat['message_thread_id']
        except KeyError:
            pass
        send_keyboard(mg_obj, chat_for_kb, msg_ids)


def copy_message(data: dict) -> None:
    """Копирует, затем отправляет пост"""
    if MediaGroup.objects.filter(
        first_message_id=data['message_id'], from_chat_id=data['from_chat_id']
        ).exists():
        target_chat = {
            'chat_id': data['chat_id'],
        }
        try:
            target_chat['message_thread_id'] = data['message_thread_id']
        except KeyError:
            pass
        send_media_group(
            MediaGroup.objects.get(
                first_message_id=data['message_id'], from_chat_id=data['from_chat_id']
            ),
            target_chat, send_kb=data['chat_id']==data['from_chat_id']
        )
        return

    method = 'copyMessage'
    url = TELEGRAM_API_URL + method
    requests.post(url, json=data, timeout=10)


def delete_post(chat_id: str, message_id: str) -> None:
    """Удаляет пост"""
    url = TELEGRAM_API_URL + f'deleteMessage?chat_id={chat_id}&message_id={message_id}'
    requests.get(url, timeout=10)


def get_or_create_media_group(mg_id, from_chat, first_message_id=None):
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


def get_media_type(message: dict) -> str:
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
