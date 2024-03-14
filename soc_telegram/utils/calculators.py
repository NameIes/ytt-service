from soc_telegram.models import Calculator, Channel
from soc_telegram.utils.telegram_api import send_message, edit_message


def update_members_count():
    for channel in Channel.objects.all():
        channel.update_members_count()


def _get_or_send_message(chat: Channel, message_id: str, calc: Calculator) -> str:
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
            channel = business.channels.first()
            data['reply_markup']['inline_keyboard'].append([{
                'text': channel.name_chat + ' | ' + str(business.get_members_count()) + ' подписчик(ов)',
                'url': channel.link
            }])

        edit_message(data)
