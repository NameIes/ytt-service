"""That module contains application configuration."""

from django.apps import AppConfig


class DbModelsConfig(AppConfig):
    """Class describing Database Models Configuration."""
    default_auto_field = "django.db.models.BigAutoField"
    name = "db_models"
    verbose_name = 'Бизнес данные'
