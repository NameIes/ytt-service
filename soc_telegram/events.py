"""That module contains events handlers"""

import json
from django.conf import settings
from soc_telegram.services import get_current_contact_person, get_current_worker, \
    get_data_for_copy, copy_message, delete_post, get_current_channel, \
    get_or_create_media_group, get_media_type, send_media_group
from soc_telegram.models import ChannelOfCoordination, MediaGroupItem, MediaGroup


def on_user_joined(message: dict):
    """
    Update the Telegram user's information in the database based on the message received.

    Args:
        message (dict): The message containing information about the new chat member.
    """
    telegram_user_name = message['message']['new_chat_member']['username']
    telegram_id = message['message']['new_chat_member']['id']
    contact_person = get_current_contact_person(telegram_user_name=telegram_user_name)
    worker = get_current_worker(telegram_user_name=telegram_user_name)

    if contact_person:
        contact_person.telegram_id = telegram_id
        contact_person.save()

        channel = contact_person.business.сhannel_of_coordination.first()
        channel.chat_id = message['message']['chat']['id']
        channel.save()

    if worker:
        worker.telegram_id = telegram_id
        worker.save()


def on_reaction(message: dict):
    """
    A function that processes a message reaction from a user.
    Takes a message dictionary as input and retrieves the telegram_id and
    contact_person associated with the user.
    It then checks if the contact_person exists and if they are the owner of the channel.
    If the contact_person is valid and the channel ownership is confirmed, it retrieves
    the data from the message and copies it.
    """
    telegram_id = message['message_reaction']['user']['id']
    contact_person = get_current_contact_person(telegram_id=telegram_id)
    chat_id = message['message_reaction']['chat']['id']
    message_id = message['message_reaction']['message_id']

    if contact_person is None:
        print('Пользователь не является контактным лицом')
        return

    if str(message['message_reaction']['user']['id']) == str(contact_person.telegram_id):
        print('Контактное лицо не может опубликовать свой же пост')
        return

    if not contact_person.business.сhannel_of_coordination.filter(chat_id=chat_id).exists():
        print('Контактное лицо не является владельцем канала для согласований')
        return

    data = get_data_for_copy(chat_id=chat_id, target_chat_id=chat_id, message_id=message_id)
    copy_message(data=data)


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


def process_default_message(message, chat_id, message_id):
    """
    A function to process a default message based on the callback data provided.

    Parameters:
        message (dict): the message data to process.
        chat_id (str): the chat ID associated with the message.
        message_id (str): the ID of the message.

    Returns:
        None
    """
    # При нажатии на опубликовать
    if message['callback_query']['data'] == 'success':
        # id канала, где будет публикация
        business = ChannelOfCoordination.objects.get(chat_id=chat_id).business
        channels = business.channels.all()

        for channel in channels:
            if channel.chat_id is None:
                print("ID канала не установлен")
                continue

            # Получить данные
            data = get_data_for_copy(
                chat_id=chat_id, target_chat_id=channel.chat_id, message_id=message_id)
            # Скопировать и опубликовать пост
            copy_message(data)

    # Удаляет пост с кнопками
    delete_post(chat_id=chat_id, message_id=message_id)


def process_media_group(message):
    """
    Process the media group from the provided message.

    Args:
        message (dict): The message containing the media group data.

    Returns:
        None
    """
    query = json.loads(message['callback_query']['data'])
    from_chat_id = message['callback_query']['message']['chat']['id']

    if query['success']:
        mg_obj = MediaGroup.objects.get(id=query['mg_id'])
        business = ChannelOfCoordination.objects.get(chat_id=mg_obj.from_chat_id).business
        for channel in business.channels.all():
            if channel.chat_id is None:
                print("ID канала не установлен")
                continue

            target_chat = {
                'chat_id': channel.chat_id
            }
            if channel.thread_id:
                target_chat['message_thread_id'] = channel.thread_id

            send_media_group(mg_obj, target_chat)

    query['msg_ids'].append(message['callback_query']['message']['message_id'])
    for msg_id in query['msg_ids']:
        delete_post(chat_id=from_chat_id, message_id=msg_id)


def on_click_button(message: dict):
    """Контактное лицо при нажатии на кнопки, публикует или отменяет пост."""
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
