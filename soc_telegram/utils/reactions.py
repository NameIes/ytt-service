"""That module contains utility functions for working with reactions"""

from django.conf import settings
from db_models.models import ContactPerson


def _is_contact_person_reacted(contact_person: ContactPerson) -> bool:
    return not (contact_person is None)


def _is_contact_person_reacted_himself(message: dict, contact_person: ContactPerson) -> bool:
    if settings.DEBUG:
        return False
    return str(message['message_reaction']['user']['id']) == str(contact_person.telegram_id)


def _is_owner_reacted(message: dict, contact_person: ContactPerson) -> bool:
    return contact_person.business.сhannel_of_coordination.filter(
        chat_id=message['message_reaction']['chat']['id']
    ).exists()


def check_reaction(message: dict) -> bool:
    contact_person = ContactPerson.objects.filter(
        telegram_id=message['message_reaction']['user']['id']
    ).first()

    if not _is_contact_person_reacted(contact_person):
        return False

    if _is_contact_person_reacted_himself(message, contact_person):
        return False

    if not _is_owner_reacted(message, contact_person):
        return False

    return True
