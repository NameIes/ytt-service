import json
from django.conf import settings
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

from soc_telegram.events import on_user_joined, on_reaction, on_user_message


@csrf_exempt
def handle_bot_events(request, secret_key):
    """
    Handle events from Telegram bot in the request and return an HTTP response.
    """
    if request.method != 'POST':
        raise Http404()

    if secret_key != settings.WEBHOOK_SECRET_KEY:
        raise Http404()

    message = json.loads(request.body.decode('utf-8'))


    if 'message' in message:
        if 'new_chat_member' in message['message']:
            on_user_joined(message=message)
        else:
            on_user_message(message=message)

    print(message)

    if 'message_reaction' in message and len(message['message_reaction']['new_reaction']) > 0:
        if '👍' in message['message_reaction']['new_reaction'][0]['emoji']:
            on_reaction(message=message)


    return HttpResponse('ok')
