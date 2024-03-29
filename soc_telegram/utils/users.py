"""That module contains utility functions for working with users"""

from db_models.models import ContactPerson, Worker


def set_contact_person_id(message: dict) -> None:
    """Данный метод устанавливает telegram_id контактного лица в соответствующую таблицу."""
    telegram_user_name = message['message']['new_chat_member']['username']
    telegram_id = message['message']['new_chat_member']['id']
    contact_person = ContactPerson.objects.filter(telegram_user_name=telegram_user_name).first()

    if contact_person:
        contact_person.telegram_id = telegram_id
        contact_person.save()


def set_worker_id(message: dict) -> None:
    """Данный метод устанавливает telegram_id сотрудника в соответствующую таблицу."""
    telegram_user_name = message['message']['new_chat_member']['username']
    telegram_id = message['message']['new_chat_member']['id']
    worker = Worker.objects.filter(telegram_user_name=telegram_user_name).first()

    if worker:
        worker.telegram_id = telegram_id
        worker.save()
