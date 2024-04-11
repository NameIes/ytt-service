"""That module contains functions that are used in the Telegram bot events handler."""

from django.conf import settings
from django.http import Http404


def check_reaction(message: dict) -> bool:
    """
    Check if the message has a specific reaction and return a boolean value.
    """
    is_put_reaction = len(message['message_reaction']['new_reaction']) > 0
    is_emoji = is_put_reaction and '👍' in message['message_reaction']['new_reaction'][0]['emoji']

    return is_emoji


def get_event_type(message: dict) -> str:
    """
    Return the type of event based on the message content.

    Args:
        message (dict): The message dictionary containing information about the event.

    Returns:
        str: The type of event based on the message content.
    """
    if 'message' in message:
        if 'new_chat_member' in message['message']:
            return 'user_joined'
        return 'user_message'

    if 'message_reaction' in message and check_reaction(message):
        return 'reaction'

    if 'callback_query' in message:
        return 'click_button'

    if 'channel_post' in message:
        return 'channel_post'

    if 'edited_message' in message:
        return 'edit_message'

    return 'unknown'


def check_method(request):
    """
    Check the method of the request and raise an Http404 exception if the method is not 'POST'.

    Args:
        request (HttpRequest): the request object

    Returns:
        None
    """
    if request.method != 'POST':
        raise Http404()


def check_secret_key(secret_key):
    """
    Check if the provided secret key matches the predefined webhook secret key.
    """
    if secret_key != settings.WEBHOOK_SECRET_KEY:
        raise Http404()
