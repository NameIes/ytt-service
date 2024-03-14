# Generated by Django 4.1 on 2024-03-14 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('soc_telegram', '0008_mediagroupitem_message_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mediagroup',
            options={'verbose_name': 'Медиа группа', 'verbose_name_plural': 'Медиа группы'},
        ),
        migrations.AlterModelOptions(
            name='mediagroupitem',
            options={'verbose_name': 'Элемент медиа группы', 'verbose_name_plural': 'Элементы медиа группы'},
        ),
        migrations.AlterField(
            model_name='mediagroup',
            name='first_message_id',
            field=models.CharField(max_length=256, verbose_name='Идентификатор первого сообщения'),
        ),
        migrations.AlterField(
            model_name='mediagroup',
            name='from_chat_id',
            field=models.CharField(max_length=256, verbose_name='Идентификатор чата'),
        ),
        migrations.AlterField(
            model_name='mediagroup',
            name='media_group_id',
            field=models.CharField(max_length=256, verbose_name='Идентификатор группы медиа'),
        ),
        migrations.AlterField(
            model_name='mediagroupitem',
            name='caption',
            field=models.CharField(blank=True, max_length=4096, null=True, verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='mediagroupitem',
            name='file_id',
            field=models.CharField(max_length=512, verbose_name='Идентификатор медиа'),
        ),
        migrations.AlterField(
            model_name='mediagroupitem',
            name='media_type',
            field=models.CharField(max_length=64, verbose_name='Тип медиа'),
        ),
        migrations.AlterField(
            model_name='mediagroupitem',
            name='message_id',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Идентификатор сообщения'),
        ),
        migrations.CreateModel(
            name='Calculator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0, verbose_name='Количество подписчиков')),
                ('message_id', models.CharField(blank=True, max_length=128, null=True, verbose_name='Идентификатор сообщения')),
                ('from_channels', models.ManyToManyField(related_name='calculates_from', to='soc_telegram.channel', verbose_name='От каналов')),
                ('in_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calculators', to='soc_telegram.channel', verbose_name='В канале')),
            ],
            options={
                'verbose_name': 'Калькулятор',
                'verbose_name_plural': 'Калькуляторы',
            },
        ),
    ]
