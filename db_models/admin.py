from django.contrib import admin

from db_models.models import Organization, Worker, Business, ContactPerson, EmailVerificationCode


@admin.register(Organization)
class OrganizationModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'inn', 'ogrn', 'adress']


@admin.register(Worker)
class WorkerModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'number_phone', 'email', 'telegram_user_name', 'telegram_id']


@admin.register(Business)
class BusinessModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'worker', 'organization']


@admin.register(ContactPerson)
class ContactPersonModelAdmin(admin.ModelAdmin):
    list_display = ['job_title', 'name', 'number_phone']


@admin.register(EmailVerificationCode)
class EmailVerificationCodeModelAdmin(admin.ModelAdmin):
    list_display = ['code', 'user', 'valid_until']
