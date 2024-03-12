"""That module contains URL patterns for soc_telegram app."""

from django.urls import path
from soc_telegram.views import handle_bot_events


urlpatterns = [
    path('handle_bot_events/<str:secret_key>/', handle_bot_events),
]
