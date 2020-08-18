from django.apps import AppConfig


class ManagerConfig(AppConfig):
    name = 'manager'

    def ready(self):
        from . import signals
