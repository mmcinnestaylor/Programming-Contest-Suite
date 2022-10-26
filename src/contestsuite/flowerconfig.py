import os


def get_secret(key, default=None):
    value = os.getenv(key, default)
    if value and os.path.isfile(value):
        with open(value) as f:
            return f.read().strip()
    return value


# Celery Flower configuration
# https://flower.readthedocs.io/en/latest/config.html

if get_secret('DEBUG'):
    debug = get_secret('DEBUG') == 'True'
else:
    debug = False

broker_api = get_secret('FLOWER_BROKER_API', 'http://rabbitmq:15672/api/vhost')

if not debug:
    basic_auth = basic_auth = [
        get_secret('FLOWER_USER', 'contestadmin') + ':' + get_secret('FLOWER_PASSWORD', 'seminoles1!')
    ]

    if get_secret('FLOWER_COOKIE_KEY'):
        cookie_secret = get_secret('FLOWER_COOKIE_KEY')

    url_prefix = get_secret('FLOWER_URL_PREFIX', 'flower')
