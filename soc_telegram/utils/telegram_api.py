import requests
from core.settings import TELEGRAM_API_URL


def send_media_group(data):
    method = 'sendMediaGroup'
    url = TELEGRAM_API_URL + method
    return requests.post(url, json=data, timeout=10).json()


def copy_message(data):
    method = 'copyMessage'
    url = TELEGRAM_API_URL + method
    return requests.post(url, json=data, timeout=10).json()


def send_message(data):
    method = 'sendMessage'
    url = TELEGRAM_API_URL + method
    return requests.post(url, json=data, timeout=10).json()
