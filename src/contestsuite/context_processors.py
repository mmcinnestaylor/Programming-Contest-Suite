from .settings import CACHE_TIMEOUT, DEBUG, GTAG


def app_settings(request):
    """
    Additional project settings added to the default context.
    https://docs.djangoproject.com/en/4.2/ref/templates/api/#writing-your-own-context-processors
    """

    return {
        'CACHE_TIMEOUT': CACHE_TIMEOUT,
        'DEBUG': DEBUG,
        'GTAG': GTAG,
        }
