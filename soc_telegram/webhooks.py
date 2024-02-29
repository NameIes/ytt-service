import requests, os
from django.conf import settings


def set_webhook():
    """
    Set the webhook for the Telegram API using the provided settings.
    """
    if os.environ.get("RUN_MAIN") == "true":
        url = settings.TELEGRAM_API_URL + "setWebhook"
        url += "?url=" + settings.WEBHOOK_HANDLE_URL
        url += '&allowed_updates=["message_reaction", "message", "callback_query", "channel_post", "chat_join_request"]'

        response = requests.post(
            url
        ).json()

        print('Webhook set with response:', response)


def delete_webhook():
    """
    Delete the webhook by sending a POST request to the Telegram API URL with the 'remove' parameter.
    """
    if os.environ.get("RUN_MAIN") == "true":
        response = requests.post(
            settings.TELEGRAM_API_URL + "setWebhook?remove=",
        ).json()

        print('Webhook deleted with response:', response)
