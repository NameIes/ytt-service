import string
import random
from django.db import models
from db_models.models import Business


def generate_code(
    size=512, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


class Website(models.Model):
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, verbose_name='Бизнес', related_name='websites'
    )
    name = models.CharField(max_length=100, verbose_name='Название')
    url = models.URLField(verbose_name='Ссылка на api для загрузки поста')
    code = models.CharField(
        max_length=100, verbose_name='Код для загрузки постов',
        editable=False, default=generate_code
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сайт'
        verbose_name_plural = 'Сайты'
