# Generated by Django 4.1 on 2024-04-10 09:12

from django.db import migrations, models
import websites.models


class Migration(migrations.Migration):

    dependencies = [
        ('websites', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='code',
            field=models.CharField(default=websites.models.generate_code, editable=False, max_length=612, verbose_name='Код для загрузки постов'),
        ),
    ]
