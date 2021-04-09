from django.apps import AppConfig


class FormularioConfig(AppConfig):
    name = 'formulario'

    def ready(self):
        import formulario.signals