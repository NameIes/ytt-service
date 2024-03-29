"""That module contains view for the Telegram bot events handler."""

import json
import logging
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from soc_telegram import events
from soc_telegram.utils import events as event_utils
from soc_telegram.utils import calculators


EVENTS = {
    'user_joined': events.on_user_joined,
    'user_message': events.on_user_message,
    'reaction': events.on_reaction,
    'click_button': events.on_click_button,
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
    except Exception as e:
        logger = logging.getLogger('django')
        logger.error(e)
        return HttpResponse('Error')

    return HttpResponse('Ok')


def handle_calculator_event(request, secret_key):
    """
    Данный метод вызывается каждые 30 минут, и обновляет количество участников в каналах,
    а так-же обновляет текст сообщений, которые содержат калькуляторы.
    """
    event_utils.check_method(request)
    event_utils.check_secret_key(secret_key)

    try:
        calculators.update_members_count()
    except Exception as e:
        logger = logging.getLogger('django')
        logger.error(e)
        return HttpResponse('Error')
    calculators.update_calc_messages()

    return HttpResponse('Ok')
