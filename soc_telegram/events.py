import requests

from core.settings import TELEGRAM_API_URL
from soc_telegram.servieces import get_current_contact_person, get_current_worker


def on_user_joined(message: dict):
    telegram_user_name = message['message']['new_chat_member']['username']
    telegram_id = message['message']['new_chat_member']['id']
    contact_person = get_current_contact_person(telegram_user_name=telegram_user_name)
    worker = get_current_worker(telegram_user_name=telegram_user_name)
    if contact_person:
        contact_person.telegram_id = telegram_id
        contact_person.save()

    if worker:
        worker.telegram_id = telegram_id
        worker.save()


def on_reaction(message: dict):
    print('Пользователь поставил реакцию')
    telegram_id = message['message_reaction']['user']['id']
    contact_person = get_current_contact_person(telegram_id=telegram_id)
    if contact_person is None:  # если пользователь не контактное лицо, он не может взаимодействовать с данной функцией
        return {'status': 404, 'msg': 'пользователь не является контактным лицом'}
    method = 'copyMessage'
    chat_id = message['message_reaction']['chat']['id']
    message_id = message['message_reaction']['message_id']
    data = {
        'chat_id': chat_id,
        'from_chat_id': chat_id,
        'message_id': message_id,
        'caption': 'Copied message',
        'reply_markup': {
            'inline_keyboard': [
                [{'text': 'Опубликовать ✅', 'callback_data': 'button1'}],
                [{'text': 'Отменить публикацию ❌', 'callback_data': 'button2'}]
            ],
            'resize_keyboard': True
        }
    }
    url = TELEGRAM_API_URL + method
    response = requests.post(url, json=data)
    result = response.json()
    print(result)



def on_user_message(message: dict):
    print('Пользователь написал сообщение')


# todo: добавить модель администратора

def on_add_main_channel():
    pass


def on_add_channel_of_coordination():
    pass
