"""That module contains events handlers"""

import json
from django.conf import settings
from soc_telegram.services import get_current_contact_person, \
    delete_post, get_current_channel, \
    get_or_create_media_group, get_media_type
from soc_telegram.models import ChannelOfCoordination, MediaGroupItem
from soc_telegram.utils.users import set_contact_person_id, set_worker_id
from soc_telegram.utils.channels import set_channel_of_coordination_id
from soc_telegram.utils.messages import remove_join_message, is_media_group, copy_media_group, \
                           copy_message, send_approve_keyboard
from soc_telegram.utils.reactions import check_reaction


def on_user_joined(message: dict):
    """
    Update the Telegram user's information in the database based on the message received.

    Args:
        message (dict): The message containing information about the new chat member.
    """
    set_contact_person_id(message)
    set_worker_id(message)
    set_channel_of_coordination_id(message)
    remove_join_message(message)


def on_reaction(message: dict):
    """
    A function that processes a message reaction from a user.
    Takes a message dictionary as input and retrieves the telegram_id and
    contact_person associated with the user.
    It then checks if the contact_person exists and if they are the owner of the channel.
    If the contact_person is valid and the channel ownership is confirmed, it retrieves
    the data from the message and copies it.
    """

    if not check_reaction(message):
        return

    if is_media_group(message):
        mg_id = copy_media_group(message, to_main_channels=False)
        send_approve_keyboard(message, is_media_group=True, mg_id=mg_id)
    else:
        mg_id = copy_message(message, to_main_channels=False)
        send_approve_keyboard(message, is_media_group=False, mg_id=mg_id)


def on_click_button(message: dict):
    """Контактное лицо при нажатии на кнопки, публикует или отменяет пост."""
    query = json.loads(message['callback_query']['data'])
    print(query)
    return

    telegram_id = message['callback_query']['from']['id']
    contact_person = get_current_contact_person(telegram_id=telegram_id)
    chat_id = message['callback_query']['message']['chat']['id']
    message_id = message['callback_query']['message']['message_id']

    if contact_person is None:
        print('Пользователь не является контактным лицом')
        return

    if message['callback_query']['data'] in ('success', 'failure'):
        process_default_message(message, chat_id, message_id)
    else:
        process_media_group(message)


def on_user_message(message: dict):
    """
    A function that processes a user message by extracting
    media group information and saving it to the database.

    Args:
        message (dict): a dictionary containing information about the user message

    Returns:
    - None
    """
    if settings.DEBUG:
        print('Пользователь написал сообщение')

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

    mg_obj = get_or_create_media_group(
        mg_id=mg_id,
        from_chat=message['message']['chat']['id'],
        first_message_id=message['message']['message_id']
    )

    m_type = get_media_type(message)
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


def on_set_channel_id(message: dict):
    """
    A function that handles setting the channel ID based on the message dictionary.
    Parameters:
    - message: a dictionary containing information about the channel post
    """
    channel_name = message['channel_post']['sender_chat']['title']
    channel = get_current_channel(name_chat=channel_name)
    channel_id = message['channel_post']['sender_chat']['id']
    message_id = message['channel_post']['message_id']

    delete_post(chat_id=channel_id, message_id=message_id)

    if channel is None or channel.chat_id is not None:
        print('Такого канала нет или id канала уже есть в бд')
        return

    channel.chat_id = channel_id
    channel.save()