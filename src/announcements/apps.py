from django.apps import AppConfig


class AnnouncementsConfig(AppConfig):
    name = 'announcements'

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        from . import signals
