from django.apps import AppConfig


class PaniavaultConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "paniavault"
    verbose_name = 'پنل تامین'

    def ready(self):
        import paniavault.signals