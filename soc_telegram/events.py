"""That module contains events handlers"""

import json
from soc_telegram.utils.users import set_contact_person_id, set_worker_id
from soc_telegram.utils.messages import remove_join_message, copy_message, \
                           send_approve_keyboard, delete_approve_keyboard, \
                           collect_message
from soc_telegram.utils.reactions import check_reaction, is_contact_person_clicked_btn


def on_user_joined(message: dict):
    """
    Данный метод вызывается, когда пользователь присоединяется к каналу с ботом.

    После присоединения пользователя проверяется наличие его username в нашей БД,
    и если он существует, то мы устанавливаем его telegram_id в соответствующую таблицу.

    После этого мы удаляем сообщение о присоединении к каналу.

    Args:
        message (dict): The message containing information about the new chat member.
    """
    set_contact_person_id(message)
    set_worker_id(message)
    remove_join_message(message)


def on_reaction(message: dict):
    """
    Данный метод вызывается при нажатии на реакцию к сообщению.
    В первую очередь проверяется кто отреагировал, и только затем начинается процесс согласования.
    """

    if not check_reaction(message):
        return

    copy_message(
        message_id=message['message_reaction']['message_id'],
        to_main_channels=False,
        from_channel=message['message_reaction']['chat']['id'],
    )

    send_approve_keyboard(
        target_chat_id=message['message_reaction']['chat']['id'],
        message_id=message['message_reaction']['message_id'],
        from_channel=message['message_reaction']['chat']['id'],
    )


def on_click_button(message: dict):
    """Контактное лицо при нажатии на кнопки, публикует или отменяет пост."""

    if not is_contact_person_clicked_btn(message):
        return

    query = json.loads(message['callback_query']['data'])

    if query['succ']:
        copy_message(
            message_id=query['mid'],
            from_channel=query['cid'],
            to_main_channels=True
        )

    delete_approve_keyboard(message)


def on_user_message(message: dict):
    """
    Данный метод вызывается при получении сообщения от пользователя, даже если
    он пишет в один канал с ботом.

    Метод сохраняет написанное сообщение в БД. Это необходимо для того, чтобы была
    возможность копировать группы файлов в другой канал, так как каждое фото, видео,
    файл в одном сообщении на самом деле разные сообщения с одним ключом группы (media_group_id).

    Args:
        message (dict): a dictionary containing information about the user message

    Returns:
    - None
    """

    collect_message(message)


def edit_message(message: dict):
    print('ААААААААААРРРРРРРИИИФААА ЕБ ВАШУ МАТЬ')