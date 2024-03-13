"""That module contains view for the Telegram bot events handler."""

import json
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from soc_telegram import events
from soc_telegram.utils import events as event_utils


EVENTS = {
    'user_joined': events.on_user_joined,
    'user_message': events.on_user_message,
    'reaction': events.on_reaction,
    'click_button': events.on_click_button,
    'channel_post': events.on_set_channel_id,
}


@csrf_exempt
def handle_bot_events(request, secret_key):
    """
    Handles bot events received in a POST request using a secret key for authentication.

    Args:
        request (HttpRequest): HttpRequest object containing the request data
        secret_key (str): Secret key for verifying the authenticity of the request

    Returns:
        HttpResponse: Response indicating the success or failure of handling the bot events
    """
    event_utils.check_method(request)
    event_utils.check_secret_key(secret_key)

    message = json.loads(request.body.decode('utf-8'))
    if settings.DEBUG:
        print(message)

    try:
        EVENTS[event_utils.get_event_type(message)](message)
    except KeyError:
        return HttpResponse('Not used')

    return HttpResponse('Ok')
