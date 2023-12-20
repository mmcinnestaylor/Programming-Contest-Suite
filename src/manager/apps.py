from django.apps import AppConfig


class ManagerConfig(AppConfig):
    name = 'manager'

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        from . import signals
