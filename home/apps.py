from django.apps import AppConfig
import importlib

class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    def ready(self):
        import home.signals # type: ignore
