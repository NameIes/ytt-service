from django.db import models
from db_models.models import Business
class Channel(models.Model):
    chat_id = models.CharField(max_length=128)
    link = models.URLField(max_length=128)
    name_chat = models.CharField(max_length=128)
    business = models.ForeignKey(Business, models.SET_NULL, null=True, blank=True, related_name="channels")

# Create your models here.
