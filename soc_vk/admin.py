from django.contrib import admin
from soc_vk.models import Group


@admin.register(Group)
class GroupModelAdmin(admin.ModelAdmin):
    """Class describing Group model in Django admin site."""

    list_display = ['name', 'group_id', 'link']
    list_filter = ['business']
