import requests, os
from django.conf import settings


def set_webhook():
    if os.environ.get("RUN_MAIN") == "true":
        url = settings.TELEGRAM_API_URL + "setWebhook"
        url += "?url=" + settings.WEBHOOK_HANDLE_URL
        url += '&allowed_updates=["message_reaction", "message"]'

        response = requests.post(
            url
        ).json()

        print('Webhook set with response:', response)


def delete_webhook():
    if os.environ.get("RUN_MAIN") == "true":
        response = requests.post(
            settings.TELEGRAM_API_URL + "setWebhook?remove=",
        ).json()

        print('Webhook deleted with response:', response)
