from django.contrib import admin
from websites.models import Website


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_filter = ['business']
    list_display = ['business', 'name', 'url', 'code']
