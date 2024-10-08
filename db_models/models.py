"""That module contains database models."""

import os
from django.db import models


class Organization(models.Model):
    """Модель описывает организацию клиента.
    Данная модель в текущий момент нигде не используется.

    Args:
        name (str): Organization name.
        inn (str): Organization INN.
        ogrn (str): Organization OGRN.
        adress (str): Organization adress.
    """
    name = models.CharField(
        max_length=128, verbose_name='Наименование организации', null=True, blank=True)
    inn = models.CharField(max_length=128, verbose_name='ИНН', null=True, blank=True)
    ogrn = models.CharField(max_length=128, verbose_name='ОГРН', null=True, blank=True)
    adress = models.CharField(max_length=128, verbose_name='Юр. адрес', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class Worker(models.Model):
    """Модель описывает нашего удаленного сотрудника.
    Данная модель в текущий момент нигде не используется.

    Args:
        name (str): Worker name.
        number_phone (str): Worker phone number.
        email (str): Worker email.
        telegram_user_name (str): Username of Worker in Telegram.
        telegram_id (str): user_id of Worker in Telegram.
    """
    name = models.CharField(max_length=128, verbose_name='ФИО работника')
    number_phone = models.CharField(max_length=32, verbose_name='Номер телефона')
    email = models.EmailField(max_length=128, verbose_name='Почта')
    telegram_user_name = models.CharField(
        max_length=128, null=True, blank=True, verbose_name='Никнейм в телеграмме')
    telegram_id = models.CharField(
        max_length=128, null=True, blank=True, verbose_name='Идентификатор в телеграмме')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'SMM-щик'
        verbose_name_plural = 'SMM-щики'


class Business(models.Model):
    """Модель описывающая бизнес (нашего клиента).

    Args:
        parent (Business): Родительский бизнес, используется для рассчета
                           подписчиков в калькуляторе.
        name (str): Business name.
        worker (Worker): SMM specialist.
        organization (Organization): Organization of a Business.
    """
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True,
        blank=True, related_name='childrens', verbose_name='Родительский бизнес')
    name = models.CharField(max_length=128, verbose_name='Наименование бизнеса')
    worker = models.ForeignKey(
        Worker, on_delete=models.SET_NULL, null=True,
        blank=True, related_name='business', verbose_name='SMM-щик')
    organization = models.ForeignKey(
        Organization, on_delete=models.SET_NULL, null=True,
        blank=True, related_name='business', verbose_name='Организация')

    def get_members_count(self):
        count_in_self = max(
            [channel.members_count for channel in self.channels.all()] + \
            [group.members_count for group in self.groups.all()]
        )

        if self.childrens.count() == 0:
            return count_in_self

        counts = []
        for business in self.childrens.all():
            counts.append(
                business.get_members_count()
            )

        return sum(counts) + count_in_self

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Бизнес'
        verbose_name_plural = 'Бизнесы'


class ContactPerson(models.Model):
    """Модель описывает контактное лицо клиента.

    Args:
        job_title (str): Job title of a Contact Person.
        name (str): Contact Person name.
        number_phone (str): Contact Person phone number.
        email (str): Contact Person email.
        telegram_user_name (str): Username of Contact Person in Telegram.
        telegram_id (str): user_id of Contact Person in Telegram.
        business (Business): Business of a Contact Person.
    """
    job_title = models.CharField(max_length=128, verbose_name='Должность')
    name = models.CharField(max_length=128, verbose_name='ФИО')
    number_phone = models.CharField(max_length=32, verbose_name='Номер телефона')
    email = models.EmailField(max_length=128, verbose_name='Почта')
    telegram_user_name = models.CharField(
        max_length=128, null=True, blank=True, verbose_name='Никнейм в телеграмме')
    telegram_id = models.CharField(
        max_length=128, null=True, blank=True, verbose_name='Идентификатор в телеграмме')
    business = models.ForeignKey(
        Business, on_delete=models.SET_NULL, null=True,
        blank=True, related_name='contact_person', verbose_name='Бизнес')
    can_post_himself = models.BooleanField(
        default=False, verbose_name='Возможность одобрять свои посты'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Контактное лицо'
        verbose_name_plural = 'Контактные лица'


class DownloadedFile(models.Model):
    """Модель необходимая для хранения файлов из телеграма.
    Необходима для создания постов в прочих ресурсах, например ВК, Pinterest и т.д.
    Так как для репоста в Telegram используется собственный метод CopyMessages, а на
    прочих ресурсах необходимо отсылать файлы.

    Args:
        filetype (str): Type of the file.
        file (str): Path to the file.
    """
    filetype = models.CharField(max_length=32, verbose_name='Тип файла')
    file = models.FileField(upload_to='downloaded_files', verbose_name='Файл')

    def delete(self, using=None, keep_parents: bool = False) -> tuple[int, dict[str, int]]:
        self.file.delete()
        return super().delete(using, keep_parents)

    def get_extension(self):
        _, extension = os.path.splitext(self.file.name)
        return extension

    class Meta:
        verbose_name = 'Загруженный файл'
        verbose_name_plural = 'Загруженные файлы'
