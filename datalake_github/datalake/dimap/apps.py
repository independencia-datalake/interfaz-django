from django.apps import AppConfig


class DimapConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dimap'

    def ready(self):
        import dimap.signals