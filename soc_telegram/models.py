"""That module describes database models."""

from django.db import models
from db_models.models import Business


class MediaGroup(models.Model):
    """That models contains information about media group.

    A post that keeps multiple photos/videos/documents/audios/animations is not a single post.
    It's a multiple posts contains in a media group.

    Args:
        from_chat_id (str): ID of the chat where the media group was created.
        first_message_id (str): ID of the first message in the media group.
        media_group_id (str): ID of the media group.
    """
    from_chat_id = models.CharField(max_length=256)
    first_message_id = models.CharField(max_length=256)
    media_group_id = models.CharField(max_length=256)

    def serialize_for_send(self) -> dict:
        """Serializes that and subitems models for send to telegram.

        Args:
            target_chat (dict): Target chat must contain `chat_id` and optional `message_thread_id`.

        Returns:
            dict: Serialized that and subitems models for send to telegram.
        """
        target_chat = []
        for i in self.items.all():
            item = {
                'type': i.media_type,
                'media': i.file_id,
            }
            if i.caption:
                item['caption'] = i.caption
            target_chat.append(item)
        return target_chat


class MediaGroupItem(models.Model):
    """Class describing media group item.

    Args:
        media_group (MediaGroup): Media group.
        media_type (str): Type of media (photos/videos/documents/audios/animations).
        caption (str): Caption of a displayed in a telegram media group post.
        file_id (str): ID of the media.
        message_id (str): ID of the sended message.
    """
    media_group = models.ForeignKey(MediaGroup, models.CASCADE, related_name='items')
    media_type = models.CharField(max_length=64)
    caption = models.CharField(max_length=4096, null=True, blank=True)
    file_id = models.CharField(max_length=512)
    message_id = models.CharField(max_length=256, null=True, blank=True)


class Channel(models.Model):
    """Class describing Telegram channel.

    Args:
        chat_id (str): ID of the channel in Telegram.
        thread_id (str): Optional. ID of the thread of topic in Telegram group.
        link (str): Link to the channel.
        name_chat (str): Name of the channel in Telegram. Must be set correctly,
                         because it's used for get chat id using bot command.
        business (Business): Business model.
    """
    chat_id = models.CharField(max_length=128, null=True, blank=True)
    thread_id = models.CharField(max_length=128, null=True, blank=True)
    link = models.URLField(max_length=128)
    name_chat = models.CharField(max_length=128, null=True, blank=True)
    business = models.ForeignKey(
        Business, models.SET_NULL, null=True, blank=True, related_name="channels")

    def __str__(self):
        return self.name_chat

    class Meta:
        verbose_name = 'Канал'
        verbose_name_plural = 'Каналы'


class ChannelOfCoordination(models.Model):
    """Class describing Telegram channel for coordination.

    Args:
        chat_id (str): ID of the channel in Telegram.
        link (str): Link to the channel.
        name_chat (str): Name of the channel in Telegram. Must be set correctly,
                         because it's used for get chat id using bot command.
        business (Business): Business model.
    """
    chat_id = models.CharField(max_length=128, null=True, blank=True)
    link = models.URLField(max_length=128)
    name_chat = models.CharField(max_length=128)
    business = models.ForeignKey(
        Business, models.SET_NULL, null=True, blank=True, related_name="сhannel_of_coordination")

    def __str__(self):
        return self.name_chat

    class Meta:
        verbose_name = 'Канал для согласования'
        verbose_name_plural = 'Каналы для согласования'
