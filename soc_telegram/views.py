import json
from django.conf import settings
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt


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
    print(message)

    return HttpResponse('ok')
