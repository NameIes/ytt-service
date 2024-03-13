import signal
import sys
from soc_telegram.utils.webhooks import delete_webhook


def on_stopping(*args):
    delete_webhook()
    sys.exit(0)

signal.signal(signal.SIGINT, on_stopping)
