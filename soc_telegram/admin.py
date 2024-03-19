"""Thas module contains Django admin site configuration."""

from django.contrib import admin
from soc_telegram.models import Channel, ChannelOfCoordination, \
                                Calculator, Message


@admin.register(Message)
class MessageModelAdmin(admin.ModelAdmin):
    """Class describing Telegram Message model in Django admin site."""

    list_display = ['coordination_channel', 'tg_message_id']
    list_filter = ['coordination_channel']


@admin.register(Channel)
class ChannelModelAdmin(admin.ModelAdmin):
    """Class describing Telegram Channel model in Django admin site."""

    list_display = ['name_chat', 'chat_id', 'thread_id', 'link']
    list_filter = ['business']


@admin.register(ChannelOfCoordination)
class ChannelOfCoordinationModelAdmin(admin.ModelAdmin):
    """Class describing Telegram Channel Of Coordination model in Django admin site."""

    list_display = ['name_chat', 'chat_id', 'link']
    list_filter = ['business']


@admin.register(Calculator)
class CalculatorModelAdmin(admin.ModelAdmin):
    """Class describing Telegram Calculator model in Django admin site."""

    list_display = ['in_channel', 'message_id']
