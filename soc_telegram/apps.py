"""That module contains application configuration."""

from django.apps import AppConfig
from soc_telegram.utils.webhooks import set_webhook


class SocTelegramConfig(AppConfig):
    """Class describing Telegram application configuration."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'soc_telegram'
    verbose_name = 'Telegram'
    verbose_name_plural = 'Telegram'

    def ready(self) -> None:
        """
        A method that sets the webhook for the current instance.
        No parameters are taken and it returns None.
        """
        set_webhook()
