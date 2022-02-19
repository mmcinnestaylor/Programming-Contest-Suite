from django.apps import AppConfig


class AnnouncementsConfig(AppConfig):
    name = 'announcements'

    def ready(self):
        from . import signals
