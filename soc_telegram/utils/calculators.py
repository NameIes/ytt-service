from soc_telegram.models import Calculator, Channel
from soc_vk.models import Group
from soc_telegram.utils.telegram_api import send_message, edit_message


def update_members_count():
    """Обновляет количество участников во всех каналах."""
    for channel in Channel.objects.all():
        channel.update_members_count()
    for group in Group.objects.all():
        group.update_members_count()


def _get_or_send_message(chat: Channel, message_id: str, calc: Calculator) -> str:
    """
    Данный метод возвращает ID сообщения калькулятора.
    В случае если сообщения нет, то оно создается и ID сохраняется в БД.
    """
    if message_id:
        return message_id

    data = {
        'chat_id': chat.chat_id,
        'text': '0',
    }
    if chat.thread_id:
        data['message_thread_id'] = chat.thread_id

    message_id = send_message(data)['result']['message_id']
    calc.message_id = message_id
    calc.save()

    return message_id


def update_calc_messages():
    """
    Данный метод редактирует сообщения калькуляторов.
    """
    calculators = Calculator.objects.all()
    for calc in calculators:
        data = {
            'chat_id': calc.in_channel.chat_id,
            'message_id': _get_or_send_message(calc.in_channel, calc.message_id, calc),
            'text': calc.get_message_text(),
            'reply_markup': {
                'inline_keyboard': []
            }
        }

        for business in calc.get_child_businesses():
            channel = business.channels.last()
            data['reply_markup']['inline_keyboard'].append([{
                'text': channel.name_chat + ' | ' + str(business.get_members_count()) + ' подписчик(ов)',
                'url': channel.link
            }])

        edit_message(data)
