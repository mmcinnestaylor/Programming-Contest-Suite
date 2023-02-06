from contestsuite import settings


def debug(request):
    # Multiple k-v pairs supported
    return {'DEBUG': settings.DEBUG}
