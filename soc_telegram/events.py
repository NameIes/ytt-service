from django.conf import settings
from soc_telegram.services import get_current_contact_person, get_current_worker, get_data_from_copy, copy_message, \
    get_id_channel_by_group, delete_post, get_current_channel


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
    Takes a message dictionary as input and retrieves the telegram_id and contact_person associated with the user.
    It then checks if the contact_person exists and if they are the owner of the channel.
    If the contact_person is valid and the channel ownership is confirmed, it retrieves the data from the message and copies it.
    """
    telegram_id = message['message_reaction']['user']['id']
    contact_person = get_current_contact_person(telegram_id=telegram_id)

    if contact_person is None:
        print('Пользователь не является контактным лицом')
        return

    chat_id = message['message_reaction']['chat']['id']

    if not contact_person.business.сhannel_of_coordination.filter(chat_id=chat_id).exists():
        print('Контактное лицо не является владельцем канала для согласований')
        return

    message_id = message['message_reaction']['message_id']

    data = get_data_from_copy(chat_id=chat_id, from_chat_id=chat_id, message_id=message_id)
    copy_message(data=data)


def on_user_message(message: dict):
    if settings.DEBUG:
        print('Пользователь написал сообщение')


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
        return None

    channel.chat_id = channel_id
    channel.save()


def on_click_button(message: dict):
    """Контактное лицо при нажатии на кнопки, публикует или отменяет пост."""
    telegram_id = message['callback_query']['from']['id']
    contact_person = get_current_contact_person(telegram_id=telegram_id)

    if contact_person is None:
        print('Пользователь не является контактным лицом')
        return

    chat_id = message['callback_query']['message']['chat']['id']
    message_id = message['callback_query']['message']['message_id']

    # При нажатии на опубликовать
    if message['callback_query']['data'] == 'success':
        # id канала, где будет публикация
        channel_id = get_id_channel_by_group(chat_id=chat_id)

        if channel_id is None:
            print("ID канала не установлен")
            return

        # Получить данные
        data = get_data_from_copy(chat_id=chat_id, from_chat_id=channel_id, message_id=message_id)
        # Скопировать и опубликовать пост
        copy_message(data)

    # Удаляет пост с кнопками
    delete_post(chat_id=chat_id, message_id=message_id)
