# Generated by Django 4.1 on 2024-03-12 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_telegram', '0007_remove_mediagroup_business'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediagroupitem',
            name='message_id',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
