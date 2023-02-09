from contestsuite import settings


def app_settings(request):
    return {
        'CACHE_TIMEOUT': settings.CACHE_TIMEOUT,
        'DEBUG': settings.DEBUG,
        'GTAG': settings.GTAG,
        }
