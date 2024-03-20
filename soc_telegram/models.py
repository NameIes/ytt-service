"""That module describes database models."""

from django.db import models
from db_models.models import Business
from soc_telegram.utils.telegram_api import get_chat_members_count


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
    use_in_calc = models.BooleanField(default=True)
    members_count = models.BigIntegerField(default=0)
    chat_id = models.CharField(max_length=128, null=True, blank=True)
    thread_id = models.CharField(max_length=128, null=True, blank=True)
    link = models.URLField(max_length=128)
    name_chat = models.CharField(max_length=128, null=True, blank=True)
    business = models.ForeignKey(
        Business, models.SET_NULL, null=True, blank=True, related_name="channels")

    def update_members_count(self):
        if not self.use_in_calc:
            if self.members_count != 0:
                self.members_count = 0
                self.save()
            return

        try:
            self.members_count = get_chat_members_count({
                'chat_id': self.chat_id,
            })['result']
            self.save()
        except KeyError as e:
            raise Exception('Telegram API error\n' + str(e) + '\nError in chat with name: ' + str(self.name_chat))

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


class Message(models.Model):
    coordination_channel = models.ForeignKey(
        ChannelOfCoordination,
        models.CASCADE,
        verbose_name='Канал для согласования',
        related_name='messages'
    )

    tg_message_id = models.CharField(max_length=64)
    message = models.JSONField()

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
