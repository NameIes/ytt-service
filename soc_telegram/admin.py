"""Thas module contains Django admin site configuration."""

from django.contrib import admin
from soc_telegram.models import Channel, ChannelOfCoordination


@admin.register(Channel)
class ChannelModelAdmin(admin.ModelAdmin):
    """Class describing Telegram Channel model in Django admin site."""

    list_display = ['chat_id', 'name_chat', 'business']


@admin.register(ChannelOfCoordination)
class ChannelOfCoordinationModelAdmin(admin.ModelAdmin):
    """Class describing Telegram Channel Of Coordination model in Django admin site."""
    list_display = ['chat_id', 'name_chat', 'business']
