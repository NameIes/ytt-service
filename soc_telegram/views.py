import json
from django.conf import settings
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def handle_reactions(request, secret_key):
    """
    Handle reactions from Telegram bot in the request and return an HTTP response.
    """
    print('TEST')

    if request.method != 'POST':
        print('POSTED')
        raise Http404()

    if secret_key != settings.WEBHOOK_SECRET_KEY:
        print('SECRET KEY NOT OK')
        print(secret_key)
        raise Http404()

    message = json.loads(request.body.decode('utf-8'))
    print(message)

    return HttpResponse('ok')
