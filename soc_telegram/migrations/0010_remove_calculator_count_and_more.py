# Generated by Django 4.1 on 2024-03-14 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_telegram', '0009_alter_mediagroup_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calculator',
            name='count',
        ),
        migrations.RemoveField(
            model_name='calculator',
            name='from_channels',
        ),
        migrations.AddField(
            model_name='calculator',
            name='message_text',
            field=models.TextField(blank=True, default='', help_text='В текст сообщения нужно добавить 3 символа "|x|" вместо которых подставится кол-во подписчиков.', verbose_name='Текст сообщения'),
        ),
        migrations.AddField(
            model_name='channel',
            name='members_count',
            field=models.BigIntegerField(default=0),
        ),
    ]
