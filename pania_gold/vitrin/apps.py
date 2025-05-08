from django.apps import AppConfig


class VitrinConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vitrin"
    verbose_name = 'پنل فروش زینتی و مستعمل'
    def ready(self):
        import vitrin.signals