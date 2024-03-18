import requests
from core.settings import TELEGRAM_API_URL


def send_media_group(data):
    method = 'sendMediaGroup'
    url = TELEGRAM_API_URL + method
    response = requests.post(url, json=data, timeout=10).json()
    # print(response)
    return response


def copy_message(data):
    method = 'copyMessage'
    url = TELEGRAM_API_URL + method
    response = requests.post(url, json=data, timeout=10).json()
    # print(response)
    return response


def send_message(data):
    method = 'sendMessage'
    url = TELEGRAM_API_URL + method
    response = requests.post(url, json=data, timeout=10).json()
    # print(response)
    return response


def delete_message(data):
    method = 'deleteMessage'
    url = TELEGRAM_API_URL + method
    response = requests.post(url, json=data, timeout=10).json()
    # print(response)
    return response


def get_chat_members_count(data):
    method = 'getChatMemberCount'
    url = TELEGRAM_API_URL + method
    response = requests.get(url, json=data, timeout=10).json()
    # print(response)
    return response


def edit_message(data):
    method = 'editMessageText'
    url = TELEGRAM_API_URL + method
    response = requests.get(url, json=data, timeout=10).json()
    # print(response)
    return response


def get_file(data):
    method = 'getFile'
    url = TELEGRAM_API_URL + method
    response = requests.get(url, json=data, timeout=10).json()
    # print(response)
    return response


def forward_message(data):
    method = 'forwardMessage'
    url = TELEGRAM_API_URL + method
    response = requests.get(url, json=data, timeout=10).json()
    # print(response)
    return response
