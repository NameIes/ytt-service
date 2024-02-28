import requests

from core.settings import TELEGRAM_API_URL
from db_models.models import ContactPerson, Worker, Business
from soc_telegram.models import ChannelOfCoordination


def get_current_contact_person(**model_param) -> ContactPerson | None:
    """
    **model_param: Поля модели по которой произойдет выборка объекта модели ContactPerson
    """
    try:
        contact_person = ContactPerson.objects.get(**model_param)
        return contact_person
    except ContactPerson.DoesNotExist:
        return None


def get_current_worker(**model_param) -> Worker | None:
    """
    **model_param: Поля модели по которой произойдет выборка объекта модели Worker
    """
    try:
        worker = Worker.objects.get(**model_param)
        return worker
    except Worker.DoesNotExist:
        return None


def get_data_from_copy(chat_id: str, from_chat_id: str, message_id: str) -> dict:
    data = {
        'chat_id': chat_id,
        'from_chat_id': from_chat_id,
        'message_id': message_id,
        'caption': 'Copied message',
    }
    if chat_id == from_chat_id:
        data.update({'reply_markup': {
            'inline_keyboard': [
                [{'text': 'Опубликовать ✅', 'callback_data': 'success'}],
                [{'text': 'Отменить публикацию ❌', 'callback_data': 'failure'}]
            ],
            'resize_keyboard': True
        }})
    return data


def copy_message(data: dict) -> None:
    method = 'copyMessage'
    url = TELEGRAM_API_URL + method
    response = requests.post(url, json=data)
    result = response.json()
    print(result)


def get_id_channel_by_group(chat_id: str):
    business = ChannelOfCoordination.objects.select_related('business').get(chat_id=chat_id)
    print(business.name_chat)
