from django.apps import AppConfig


class FarmaciaConfig(AppConfig):
    name = 'farmacia'

    def ready(self):
        import farmacia.signals