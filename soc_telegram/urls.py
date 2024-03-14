"""That module contains URL patterns for soc_telegram app."""

from django.urls import path
from soc_telegram.views import handle_bot_events, handle_calculator_event


urlpatterns = [
    path('handle_bot_events/<str:secret_key>/', handle_bot_events),
    path('handle_calculator_event/<str:secret_key>/', handle_calculator_event),
]
