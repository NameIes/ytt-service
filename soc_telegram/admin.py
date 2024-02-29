from django.contrib import admin

from soc_telegram.models import Channel, ChannelOfCoordination


@admin.register(Channel)
class ChannelModelAdmin(admin.ModelAdmin):
    list_display = ['chat_id', 'name_chat', 'business']


@admin.register(ChannelOfCoordination)
class ChannelOfCoordinationModelAdmin(admin.ModelAdmin):
    list_display = ['chat_id', 'name_chat', 'business']
