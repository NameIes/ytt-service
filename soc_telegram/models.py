from django.db import models
from db_models.models import Business


class Channel(models.Model):
    chat_id = models.CharField(max_length=128, null=True, blank=True)
    link = models.URLField(max_length=128)
    name_chat = models.CharField(max_length=128, null=True, blank=True)
    business = models.ForeignKey(Business, models.SET_NULL, null=True, blank=True, related_name="channels")

    def __str__(self):
        return self.name_chat

    class Meta:
        verbose_name = 'Канал'
        verbose_name_plural = 'Каналы'


class ChannelOfCoordination(models.Model):
    chat_id = models.CharField(max_length=128)
    link = models.URLField(max_length=128)
    name_chat = models.CharField(max_length=128)
    business = models.ForeignKey(Business, models.SET_NULL, null=True, blank=True, related_name="сhannel_of_coordination")

    def __str__(self):
        return self.name_chat

    class Meta:
        verbose_name = 'Канал для согласования'
        verbose_name_plural = 'Каналы для согласования'
