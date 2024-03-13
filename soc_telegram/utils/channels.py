"""That module contains utility functions for working with channels"""

from db_models.models import ContactPerson


def set_channel_of_coordination_id(message: dict) -> None:
    contact_person_id = message['message']['new_chat_member']['id']
    contact_person = ContactPerson.objects.filter(telegram_id=contact_person_id).first()

    if contact_person:
        channel = contact_person.business.сhannel_of_coordination.first()
        channel.chat_id = message['message']['chat']['id']
        channel.save()
