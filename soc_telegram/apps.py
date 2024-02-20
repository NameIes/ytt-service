from django.apps import AppConfig
from soc_telegram.webhooks import set_webhook


class SocTelegramConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'soc_telegram'
    verbose_name = 'Telegram'
    verbose_name_plural = 'Telegram'

    def ready(self) -> None:
        set_webhook()
