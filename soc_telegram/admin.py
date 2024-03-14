"""Thas module contains Django admin site configuration."""

from django.contrib import admin
from soc_telegram.models import Channel, ChannelOfCoordination, MediaGroup, MediaGroupItem, \
                                Calculator


class MediaGroupItemInline(admin.TabularInline):
    """Class describing MediaGroupItem inline model in Django admin site."""

    model = MediaGroupItem
    extra = 1


@admin.register(MediaGroup)
class MediaGroupModelAdmin(admin.ModelAdmin):
    """Class describing MediaGroup model in Django admin site."""

    inlines = [
        MediaGroupItemInline
    ]


@admin.register(Channel)
class ChannelModelAdmin(admin.ModelAdmin):
    """Class describing Telegram Channel model in Django admin site."""

    list_display = ['business', 'name_chat', 'chat_id', 'thread_id', 'link']


@admin.register(ChannelOfCoordination)
class ChannelOfCoordinationModelAdmin(admin.ModelAdmin):
    """Class describing Telegram Channel Of Coordination model in Django admin site."""

    list_display = ['business', 'name_chat', 'chat_id', 'link']


@admin.register(Calculator)
class CalculatorModelAdmin(admin.ModelAdmin):
    """Class describing Telegram Calculator model in Django admin site."""

    list_display = ['in_channel', 'message_id']
