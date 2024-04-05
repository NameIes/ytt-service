from django.urls import path
from db_models import views


urlpatterns = [
    path('send_post/', views.send),
    # path('', views.index),
]
