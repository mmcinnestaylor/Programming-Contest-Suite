"""
Django settings for contestsuite project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os


def get_secret(key, default=None):
    value = os.getenv(key, default)
    if value and os.path.isfile(value):
        with open(value) as f:
            return f.read().strip()
    return value


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ

SECRET_KEY = get_secret('SECRET_KEY', '86@j2=z!=&1r_hoqboog1#*mb$jx=9mf0uw#hrs@lw&7m34sqz')

# SECURITY WARNING: don't run with debug turned on in production!

if get_secret('DEBUG'):
    DEBUG = get_secret('DEBUG') == 'True'
else:
    DEBUG = False


# Allowed Hosts and Origins

ALLOWED_HOSTS = []
if DEBUG:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '[::1]']

if os.getenv('ALLOWED_HOSTS'):
    ALLOWED_HOSTS = ALLOWED_HOSTS + get_secret('ALLOWED_HOSTS').split(',')
    CSRF_TRUSTED_ORIGINS = [
        'https://'+hostname if 'https://' not in hostname else hostname for hostname in ALLOWED_HOSTS]


# Application definition

INSTALLED_APPS = [
    # Django built-ins
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # User defined
    'announcements.apps.AnnouncementsConfig',
    'checkin.apps.CheckinConfig',
    'contestadmin.apps.ContestAdminConfig',
    'core.apps.CoreConfig',
    'lfg.apps.LfgConfig',
    'manager.apps.ManagerConfig',
    'register.apps.RegisterConfig',
    # 3rd party packages
    'django_celery_beat',
    'import_export',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'contestsuite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                #'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.app_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'contestsuite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# Parse database connection url strings like psql://user:pass@127.0.0.1:8458/db
# read os.environ['DATABASE_URL'] and raises ImproperlyConfigured exception if not found

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': get_secret('SQL_HOST', 'mariadb'),
        'PORT': get_secret('SQL_PORT', '3306'),
        'NAME': get_secret('SQL_DATABASE', 'contestsuite'),
        'USER': get_secret('SQL_USER', 'contestadmin'),
        'PASSWORD': get_secret('SQL_PASSWORD', 'seminoles1!'),
        'OPTIONS': {'charset': 'utf8mb4'},
        'TIME_ZONE': 'America/New_York',
        'AUTOCOMMIT': True,
        'CONN_MAX_AGE': 0,
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# Celery
# https://docs.celeryproject.org/en/stable/getting-started/first-steps-with-celery.html#configuration
 
CELERY_BROKER_URL = get_secret('CELERY_BROKER', 'amqp://rabbitmq:5672')
CELERY_RESULT_BACKEND = get_secret('CELERY_BACKEND', 'redis://redis:6379/1')
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = get_secret('CELERY_TIMEZONE', 'America/New_York')
CELERY_ENABLE_UTC = True

# Celery Beat
# https://celery-safwan.readthedocs.io/en/latest/reference/celery.beat.html

CELERY_BEAT_SCHEDULE = {
    'cleanup-lfg-rosters': { 
         'task': 'lfg.tasks.cleanup_lfg_rosters', 
         'schedule': 600.0,
        },
    'scrape-discord-members': { 
         'task': 'lfg.tasks.scrape_discord_members', 
         'schedule': 1800.0,
        },
    'verify-lfg-profiles': { 
        'task': 'lfg.tasks.verify_lfg_profiles', 
        'schedule': 600.0,
    },          
}


# Cache
# https://docs.djangoproject.com/en/2.2/ref/settings/#caches

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': get_secret('CACHE_LOCATION', 'redis://redis:6379/0'),
    }
}

if DEBUG:
    CACHE_TIMEOUT = int(get_secret('CACHE_TIMEOUT', 0))
else:
    CACHE_TIMEOUT = int(get_secret('CACHE_TIMEOUT', 300))


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = get_secret('TIME_ZONE', 'America/New_York')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "assets"),
]


# Uploaded files (TSV)

MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Redirect to home URL after login (Default redirects to /accounts/profile/)

LOGIN_REDIRECT_URL = '/manage/'


# Sessions
# https://docs.djangoproject.com/en/3.2/topics/http/sessions/

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

if not DEBUG:
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# Messages
# https://docs.djangoproject.com/en/3.2/ref/contrib/messages/

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


# Email
# https://docs.djangoproject.com/en/3.1/topics/email/

if DEBUG:
    EMAIL_BACKEND = get_secret('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
else:
    EMAIL_BACKEND = get_secret('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
      
EMAIL_HOST = get_secret('EMAIL_HOST', None)
EMAIL_PORT = int(get_secret('EMAIL_PORT', 587))
EMAIL_HOST_USER = get_secret('EMAIL_USER', None)
EMAIL_HOST_PASSWORD = get_secret('EMAIL_PASSWORD', None)

if get_secret('EMAIL_USE_SSL'):
    EMAIL_USE_SSL = get_secret('EMAIL_USE_SSL') == 'True'
else:
    EMAIL_USE_SSL = False

if get_secret('EMAIL_USE_TLS'):
    EMAIL_USE_TLS = get_secret('EMAIL_USE_TLS') == 'True'
else:
    EMAIL_USE_TLS = False

DEFAULT_FROM_EMAIL = get_secret(
    'DEFAULT_FROM_EMAIL', 'ACM at FSU Programming Contest<acm@cs.fsu.edu>')


# Discord
# https://discordpy.readthedocs.io/en/stable/

ANNOUNCEMENT_WEBHOOK_URL = get_secret('ANNOUNCEMENT_WEBHOOK_URL', None)
BOT_CHANNEL_WEBHOOK_URL = get_secret('BOT_CHANNEL_WEBHOOK_URL', None)
GUILD_ID = int(get_secret('GUILD_ID', 0))
SCRAPE_BOT_TOKEN = get_secret('SCRAPE_BOT_TOKEN', None)


# DOMjudge Status Button

DOMJUDGE_URL = get_secret('DOMJUDGE_URL', 'https://domjudge.cs.fsu.edu/public')


# Hashid Fields
# https://pypi.org/project/django-hashid-field/

HASHID_FIELD_SALT = get_secret(
    'HASHID_FIELD_SALT', '0s97rx*t4%68jell&lw3^)97o*kr*+*2o^(76q)ix+ilc!4ax#')


# Google Analytics

GTAG = get_secret('GTAG')

