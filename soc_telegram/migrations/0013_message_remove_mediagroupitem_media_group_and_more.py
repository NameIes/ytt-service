# Generated by Django 4.1 on 2024-03-19 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('soc_telegram', '0012_channel_use_in_calc'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_message_id', models.CharField(max_length=64)),
                ('message', models.JSONField()),
                ('coordination_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='soc_telegram.channelofcoordination', verbose_name='Канал для согласования')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
        migrations.RemoveField(
            model_name='mediagroupitem',
            name='media_group',
        ),
        migrations.DeleteModel(
            name='MediaGroup',
        ),
        migrations.DeleteModel(
            name='MediaGroupItem',
        ),
    ]
