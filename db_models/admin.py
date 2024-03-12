"""Django admin site configuration."""

from django.contrib import admin
from db_models.models import Organization, Worker, Business, ContactPerson


@admin.register(Organization)
class OrganizationModelAdmin(admin.ModelAdmin):
    """Class describing Organization model in Django admin site."""

    list_display = ['name', 'inn', 'ogrn', 'adress']


@admin.register(Worker)
class WorkerModelAdmin(admin.ModelAdmin):
    """Class describing Worker model in Django admin site."""

    list_display = ['name', 'number_phone', 'email', 'telegram_user_name', 'telegram_id']


@admin.register(Business)
class BusinessModelAdmin(admin.ModelAdmin):
    """Class describing Business model in Django admin site."""

    list_display = ['name', 'worker', 'organization']


@admin.register(ContactPerson)
class ContactPersonModelAdmin(admin.ModelAdmin):
    """Class describing ContactPerson model in Django admin site."""

    list_display = ['job_title', 'name', 'number_phone']
