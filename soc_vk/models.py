from django.db import models
from db_models.models import Business
from core.settings import VK_SESSION


class Group(models.Model):
    business = models.ForeignKey(
        Business, on_delete=models.SET_NULL, verbose_name='Бизнес',
        related_name='groups', null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name='Название группы')
    link = models.CharField(max_length=255, verbose_name='Ссылка на группу')
    members_count = models.BigIntegerField(
        default=0, verbose_name='Количество участников', editable=False)
    group_id = models.CharField(max_length=128, verbose_name='ID группы')

    def update_members_count(self):
        self.members_count = VK_SESSION.groups.getById(
            group_id=int(self.group_id), fields='members_count'
        )[0]['members_count']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'