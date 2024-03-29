"""That module describes database models."""

from django.db import models
from db_models.models import Business
from soc_telegram.utils.telegram_api import get_chat_members_count, get_file


class Channel(models.Model):
    """Модель хранит данные о телеграм каналах.

    Args:
        is_calc_channel (bool): Является ли канал каналом только для размещения калькулятора.
        use_in_calc (bool): Признак использования канала при расчете подписчиков.
        members_count (int): Количество участников канала.
        chat_id (str): ID чата в телеграме.
        thread_id (str): Optional. ID топика в телеграме.
        link (str): Ссылка на канал.
        name_chat (str): Название канала в телеграме.
        business (Business): Бизнес (клиент) к которому относится канал.
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
        """Данный метод обновляет количество участников канала используя Telegram Api."""
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
    """Модель описывающая калькулятор.

    Сам калькулятор представляет собой канал с одним сообщением в котором
    есть текст "С нами уже |x| подписчиков!" где |x| - количество подписчиков.
    И есть кнопки (inline_keyboard) с названиями и ссылками на подканалы.

    Args:
        message_id (str): ID редактируемого сообщения.
        in_channel (Channel): Канал (или топик канала) в котором расположен калькулятор.
        message_text (str): Текст сообщения.
    """
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
        """Данный метод возвращает дочерние бизнесы канала."""
        return self.in_channel.business.childrens.all()

    def get_count(self) -> int:
        """Данный метод возвращает кол-во подписчиков канала и подканалов."""
        return self.in_channel.business.get_members_count()

    def get_message_text(self) -> str:
        """
        Данный метод возвращает текст сообщения,
        где |x| заменяется количеством подписчиков.
        """
        return self.message_text.replace('|x|', str(self.get_count()))

    class Meta:
        verbose_name = 'Калькулятор'
        verbose_name_plural = 'Калькуляторы'


class Message(models.Model):
    """Данная модель хранит сообщения пользователей в чистом виде (в том виде, как
    они приходят от бота).

    Сообщения сохраняются только из каналов согласования.

    Модель используется для обработки групп сообщений, так как группа сообщений (сообщение
    с несколькими картинками, видео, файлами) на самом деле является несколькими сообщениями
    с одним ключом группы (media_group_id).

    Args:
        coordination_channel (ChannelOfCoordination): Модель канала для согласования.
        tg_message_id (str): ID сообщения в телеграмме.
        message (dict): Сообщение в чистом виде.
    """
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

    def get_text(self) -> str | None:
        """Данный метод возвращает текст сообщения либо None."""
        if 'text' in self.message['message']:
            return self.message['message']['text']

        if 'caption' in self.message['message']:
            return self.message['message']['caption']

        return None

    def get_file_url(self):
        """Данный метод возвращает file_id файла либо None."""
        if 'document' in self.message['message']:
            return 'document', get_file({
                'file_id': self.message['message']['document']['file_id'],
            })

        if 'photo' in self.message['message']:
            return 'photo', get_file({
                'file_id': self.message['message']['photo'][-1]['file_id'],
            })

        if 'video' in self.message['message']:
            return 'video', get_file({
                'file_id': self.message['message']['video']['file_id'],
            })

        return None
