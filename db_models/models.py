from django.db import models

class Business(models.Model):
    name = models.CharField(max_length=128)
# Create your models here.
