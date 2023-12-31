from contestsuite import settings


def app_settings(request):
    """
    Additional project settings added to the default context.
    https://docs.djangoproject.com/en/4.2/ref/templates/api/#writing-your-own-context-processors
    """

    return {
        'CACHE_TIMEOUT': settings.CACHE_TIMEOUT,
        'DEBUG': settings.DEBUG,
        'GTAG': settings.GTAG,
        }
