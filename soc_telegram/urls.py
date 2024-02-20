from django.urls import path
from soc_telegram.views import handle_reactions


urlpatterns = [
    path('handle_reactions/<str:secret_key>/', handle_reactions),
]
