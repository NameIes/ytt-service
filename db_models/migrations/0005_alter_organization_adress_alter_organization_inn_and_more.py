# Generated by Django 4.1 on 2024-03-01 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_models', '0004_remove_contactperson_permission_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='adress',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Юр. адрес'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='inn',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='ИНН'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Наименование организации'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='ogrn',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='ОГРН'),
        ),
    ]
