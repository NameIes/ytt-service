# Generated by Django 4.1 on 2024-03-26 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_models', '0009_downloadedfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='downloadedfile',
            name='filetype',
            field=models.CharField(default='photo', max_length=32, verbose_name='Тип файла'),
            preserve_default=False,
        ),
    ]
