# Generated by Django 4.1 on 2024-03-14 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_telegram', '0011_channel_is_calc_channel'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='use_in_calc',
            field=models.BooleanField(default=True),
        ),
    ]
