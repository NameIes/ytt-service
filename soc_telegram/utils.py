def check_reaction(message: dict) -> bool:
    """
    Check if the message has a specific reaction and return a boolean value.
    """
    is_put_reaction = len(message['message_reaction']['new_reaction']) > 0
    is_emoji = is_put_reaction and '👍' in message['message_reaction']['new_reaction'][0]['emoji']

    return is_emoji


def get_event_type(message: dict) -> str:
    """
    Return the type of event based on the message content.

    Args:
        message (dict): The message dictionary containing information about the event.

    Returns:
        str: The type of event based on the message content.
    """
    if 'message' in message:
        if 'new_chat_member' in message['message']:
            return 'user_joined'
        return 'user_message'

    if 'message_reaction' in message and check_reaction(message):
        return 'reaction'

    if 'callback_query' in message:
        return 'click_button'

    if 'channel_post' in message:
        if 'entities' in message['channel_post'] and message['channel_post']['text'] == '/set-channel':
            return 'set_channel_id'

    return 'unknown'
