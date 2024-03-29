"""That module contains utility functions for working with reactions"""

import logging
from django.conf import settings
from db_models.models import ContactPerson
from soc_telegram.models import ChannelOfCoordination, Message


def _is_contact_person_reacted(contact_person: ContactPerson) -> bool:
    """
    Данный метод проверяет является ли пользователь
    поставивший реакцию контактным лицом.
    """
    return not (contact_person is None)


def _is_contact_person_reacted_himself(message: dict, contact_person: ContactPerson) -> bool:
    """
    Данный метод проверяет является ли пользователь отправивший реакцию, отправителем сообщения.
    Это необходимо для того, чтобы клиент не мог самостоятельно опубликовать свои посты.

    Исключения:
    - Данный метод всегда возвращает False в режиме отладки Django.
    - Данный метод всегда возвращает False, если у контактноого лица установлено разрешение в БД.
    """
    if settings.DEBUG:
        return False
    if contact_person.can_post_himself:
        return False
    sender_id = Message.objects.filter(
        tg_message_id=message['message_reaction']['message_id']
    ).first().message['message']['from']['id']
    return str(sender_id) == str(contact_person.telegram_id)


def _is_owner_reacted(message: dict, contact_person: ContactPerson) -> bool:
    """
    Данный метод проверяет состоит ли контактное лицо в бизнесе.
    Этот метод необходим на случай если контактное лицо другого бизнеса
    является участником канала для согласований для другого бизнеса.
    (На случай если наш директор захочет подписаться на другие каналы
    для согласований, чтобы посмотреть процесс работы).
    """
    return contact_person.business.сhannel_of_coordination.filter(
        chat_id=message['message_reaction']['chat']['id']
    ).exists()


def check_reaction(message: dict) -> bool:
    """
    Данный метод объединяет три метода проверки реакции описанные выше.
    """
    try:
        cofc = ChannelOfCoordination.objects.get(
            chat_id=message['message_reaction']['chat']['id'],
        )
        contact_person = cofc.business.contact_person.filter(
            telegram_id=message['message_reaction']['user']['id']
        ).first()
    except Exception:
        return False

    if not _is_contact_person_reacted(contact_person):
        logger = logging.getLogger('django')
        logger.error('Реакция не от контактного лица')
        return False

    if _is_contact_person_reacted_himself(message, contact_person):
        logger = logging.getLogger('django')
        logger.error('Контактное лицо отреагировало на свой пост')
        return False

    if not _is_owner_reacted(message, contact_person):
        logger = logging.getLogger('django')
        logger.error('Контактное лицо не является владельцем канала')
        return False

    return True


def is_contact_person_clicked_btn(message):
    """
    Данный метод проверяет, была ли нажата кнопка контактным лицом.
    """
    try:
        cofc = ChannelOfCoordination.objects.get(
            chat_id=message['callback_query']['message']['chat']['id']
        )
    except ChannelOfCoordination.DoesNotExist:
        return False

    return cofc.business.contact_person.filter(
        telegram_id=message['callback_query']['from']['id']
    ).exists()
