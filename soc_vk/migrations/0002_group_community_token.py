# Generated by Django 4.1 on 2024-04-10 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_vk', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='community_token',
            field=models.CharField(blank=True, default='', max_length=1024, verbose_name='Токен группы'),
        ),
    ]
