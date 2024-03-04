from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=128, verbose_name='Наименование организации', null=True, blank=True)
    inn = models.CharField(max_length=128, verbose_name='ИНН', null=True, blank=True)
    ogrn = models.CharField(max_length=128, verbose_name='ОГРН', null=True, blank=True)
    adress = models.CharField(max_length=128, verbose_name='Юр. адрес', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class Worker(models.Model):
    name = models.CharField(max_length=128, verbose_name='ФИО работника')
    number_phone = models.CharField(max_length=32, verbose_name='Номер телефона')
    email = models.EmailField(max_length=128, verbose_name='Почта')
    telegram_user_name = models.CharField(max_length=128, null=True, blank=True, verbose_name='Никнейм в телеграмме')
    telegram_id = models.CharField(max_length=128, null=True, blank=True, verbose_name='Идентификатор в телеграмме')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'SMM-щик'
        verbose_name_plural = 'SMM-щики'


class Business(models.Model):
    name = models.CharField(max_length=128, verbose_name='Наименование бизнеса')
    worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True, related_name='business', verbose_name='работяга')
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, related_name='business', verbose_name='организация')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Бизнес'
        verbose_name_plural = 'Бизнесы'


class ContactPerson(models.Model):
    job_title = models.CharField(max_length=128, verbose_name='Должность Жоб тайтл')
    name = models.CharField(max_length=128, verbose_name='ФИО')
    number_phone = models.CharField(max_length=32, verbose_name='Номер телефона')
    email = models.EmailField(max_length=128, verbose_name='Почта')
    telegram_user_name = models.CharField(max_length=128, null=True, blank=True, verbose_name='Никнейм в телеграмме')
    telegram_id = models.CharField(max_length=128, null=True, blank=True, verbose_name='Идентификатор в телеграмме')
    business = models.ForeignKey(Business, on_delete=models.SET_NULL, null=True, blank=True, related_name='contact_person', verbose_name='Бизнес')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Контактное лицо'
        verbose_name_plural = 'Контактные лица'
