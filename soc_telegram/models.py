from django.db import models
from db_models.models import Business


class MediaGroup(models.Model):
    from_chat_id = models.CharField(max_length=256)
    first_message_id = models.CharField(max_length=256)
    media_group_id = models.CharField(max_length=256)

    def serialize_for_send(self, target_chat):
        target_chat['media'] = []
        for i in self.items.all():
            item = {
                'type': i.media_type,
                'media': i.file_id,
            }
            if i.caption:
                item['caption'] = i.caption
            target_chat['media'].append(item)
        return target_chat


class MediaGroupItem(models.Model):
    media_group = models.ForeignKey(MediaGroup, models.CASCADE, related_name='items')
    media_type = models.CharField(max_length=64)
    caption = models.CharField(max_length=4096, null=True, blank=True)
    file_id = models.CharField(max_length=512)
    message_id = models.CharField(max_length=256, null=True, blank=True)


class Channel(models.Model):
    chat_id = models.CharField(max_length=128, null=True, blank=True)
    thread_id = models.CharField(max_length=128, null=True, blank=True)
    link = models.URLField(max_length=128)
    name_chat = models.CharField(max_length=128, null=True, blank=True)
    business = models.ForeignKey(Business, models.SET_NULL, null=True, blank=True, related_name="channels")

    def __str__(self):
        return self.name_chat

    class Meta:
        verbose_name = 'Канал'
        verbose_name_plural = 'Каналы'


class ChannelOfCoordination(models.Model):
    chat_id = models.CharField(max_length=128, null=True, blank=True)
    link = models.URLField(max_length=128)
    name_chat = models.CharField(max_length=128)
    business = models.ForeignKey(Business, models.SET_NULL, null=True, blank=True, related_name="сhannel_of_coordination")

    def __str__(self):
        return self.name_chat

    class Meta:
        verbose_name = 'Канал для согласования'
        verbose_name_plural = 'Каналы для согласования'
