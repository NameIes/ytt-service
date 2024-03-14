"""That module contains events handlers"""

import json
from soc_telegram.utils.users import set_contact_person_id, set_worker_id
from soc_telegram.utils.channels import set_channel_of_coordination_id
from soc_telegram.utils.messages import remove_join_message, is_media_group, copy_media_group, \
                           copy_message, send_approve_keyboard, delete_approve_keyboard, \
                           collect_media_group
from soc_telegram.utils.reactions import check_reaction, is_contact_person_clicked_btn


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

    message_id = message['message_reaction']['message_id']
    chat_id = message['message_reaction']['chat']['id']

    if is_media_group(message_id, chat_id):
        mg_id = copy_media_group(message_id=message_id, chat_id=chat_id, to_main_channels=False)
        send_approve_keyboard(message, is_media_group=True, mg_id=mg_id)
    else:
        mg_id = copy_message(message_id=message_id, chat_id=chat_id, to_main_channels=False)
        send_approve_keyboard(message, is_media_group=False, mg_id=mg_id)


def on_click_button(message: dict):
    """Контактное лицо при нажатии на кнопки, публикует или отменяет пост."""
    query = json.loads(message['callback_query']['data'])

    if not is_contact_person_clicked_btn(message):
        return

    if query['success']:
        if query['type'] == 'media_group':
            copy_media_group(
                mg_id=query['mg_id'],
                chat_id=message['callback_query']['message']['chat']['id'],
                to_main_channels=True
            )
        if query['type'] == 'message':
            copy_message(
                message_id=query['mg_id'],
                chat_id=message['callback_query']['message']['chat']['id'],
                to_main_channels=True
            )

    delete_approve_keyboard(message)


def on_user_message(message: dict):
    """
    A function that processes a user message by extracting
    media group information and saving it to the database.

    Args:
        message (dict): a dictionary containing information about the user message

    Returns:
    - None
    """

    collect_media_group(message)
