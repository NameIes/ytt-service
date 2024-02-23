from db_models.models import ContactPerson, Worker
from soc_telegram.models import ChannelOfCoordination


def on_user_joined(message: dict):
    telegram_user_name = message['message']['new_chat_member']['username']
    telegram_id = message['message']['new_chat_member']['id']

    if ContactPerson.objects.filter(telegram_user_name=telegram_user_name).count() > 0:
        contact_person = ContactPerson.objects.get(telegram_user_name=telegram_user_name)
        contact_person.telegram_id = telegram_id
        contact_person.save()

    if Worker.objects.filter(telegram_user_name=telegram_user_name).count() > 0:
        worker = Worker.objects.get(telegram_user_name=telegram_user_name)
        worker.telegram_id = telegram_id
        worker.save()


def on_reaction():
    print('Пользователь поставил реакцию')


def on_user_message(message: dict):
    print('Пользователь написал сообщение')


# todo: добавить модель администратора

def on_add_main_channel():
    pass


def on_add_channel_of_coordination():
    pass
