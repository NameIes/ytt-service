"""That module describes database models."""

from django.db import models
from db_models.models import Business
from soc_telegram.utils.telegram_api import get_chat_members_count


class MediaGroup(models.Model):
    """That models contains information about media group.

    A post that keeps multiple photos/videos/documents/audios/animations is not a single post.
    It's a multiple posts contains in a media group.

    Args:
        from_chat_id (str): ID of the chat where the media group was created.
        first_message_id (str): ID of the first message in the media group.
        media_group_id (str): ID of the media group.
    """
    from_chat_id = models.CharField(max_length=256, verbose_name='Идентификатор чата')
    first_message_id = models.CharField(max_length=256, verbose_name='Идентификатор первого сообщения')
    media_group_id = models.CharField(max_length=256, verbose_name='Идентификатор группы медиа')

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

    class Meta:
        verbose_name = 'Медиа группа'
        verbose_name_plural = 'Медиа группы'


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
    media_type = models.CharField(max_length=64, verbose_name='Тип медиа')
    caption = models.CharField(max_length=4096, null=True, blank=True, verbose_name='Текст')
    file_id = models.CharField(max_length=512, verbose_name='Идентификатор медиа')
    message_id = models.CharField(max_length=256, null=True, blank=True, verbose_name='Идентификатор сообщения')

    class Meta:
        verbose_name = 'Элемент медиа группы'
        verbose_name_plural = 'Элементы медиа группы'


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
    is_calc_channel = models.BooleanField(default=False)
    members_count = models.BigIntegerField(default=0)
    chat_id = models.CharField(max_length=128, null=True, blank=True)
    thread_id = models.CharField(max_length=128, null=True, blank=True)
    link = models.URLField(max_length=128)
    name_chat = models.CharField(max_length=128, null=True, blank=True)
    business = models.ForeignKey(
        Business, models.SET_NULL, null=True, blank=True, related_name="channels")

    def update_members_count(self):
        self.members_count = get_chat_members_count({
            'chat_id': self.chat_id,
        })['result']
        self.save()

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


class Calculator(models.Model):
    message_id = models.CharField(
        max_length=128, null=True, blank=True, verbose_name='Идентификатор сообщения')
    in_channel = models.ForeignKey(
        Channel, models.CASCADE, verbose_name='В канале', related_name='calculators')
    message_text = models.TextField(
        default='',
        blank=True,
        verbose_name='Текст сообщения',
        help_text='В текст сообщения нужно добавить 3 символа ' + \
            '"|x|" вместо которых подставится кол-во подписчиков.'
    )

    def get_child_businesses(self):
        return self.in_channel.business.childrens.all()

    def get_count(self):
        return self.in_channel.business.get_members_count()

    def get_message_text(self):
        return self.message_text.replace('|x|', str(self.get_count()))

    class Meta:
        verbose_name = 'Калькулятор'
        verbose_name_plural = 'Калькуляторы'
