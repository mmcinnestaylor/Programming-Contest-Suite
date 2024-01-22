---
title: Configuration
layout: default
nav_order: 2
---

# Configuration

The project settings file[^1] can be modified with user specified values through the use of environment variables. Environment variable values may be passed directly or as the contents of a file. In the latter case, the path of the file should be passed as a variable's value. Environment variable values may be stored and passed as [Docker Secrets](https://docs.docker.com/engine/swarm/secrets/).

{: .note-title }
> Default Values
>
> **(D)**: debug mode  
> **(P)**: production mode 

## Django

### General

Variable | Default | Description
---|---|---
SECRET_KEY | a long string[^2] | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-SECRET_KEY)
DEBUG | False | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-DEBUG) 
ALLOWED_HOSTS | [] | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#allowed-hosts)
TIME_ZONE | America/New_York | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-TIME_ZONE)


### Cache

Variable | Default | Description
---|---|---
CACHE_LOCATION | redis://redis:6379/0 | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#location)
CACHE_TIMEOUT | 0 **(D)**, 300 **(P)** | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#timeout)



### Database 

Variable | Default | Description
---|---|---
SQL_HOST | mariadb | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#host)
SQL_PORT | 3306 | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#port)
SQL_DATABASE | contestsuite | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#name)
SQL_USER | contestadmin | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#user)
SQL_PASSWORD | seminoles1! | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#password)
SQL_TIMEZONE | America/New_York | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#time-zone) 


### Email

Variable | Default | Description
---|---|---
EMAIL_BACKEND | <console **(D)** smtp **(P)**>.EmailBackend | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#email-backend)
EMAIL_HOST | None | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#email-host)
EMAIL_PORT | 587 | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#email-port)
EMAIL_HOST_USER | None | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#email-host-user)
EMAIL_HOST_PASSWORD | None | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#email-host-password)
EMAIL_USE_SSL | False | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#email-use-ssl)
EMAIL_USE_TLS | False | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#email-use-tls)
DEFAULT_FROM_EMAIL | acm@cs.fsu.edu | [Docs](https://docs.djangoproject.com/en/4.2/ref/settings/#default-from-email)

## Celery

Variable | Default | Description
---|---|---
CELERY_BROKER | amqp://rabbitmq:5672 | [Docs](https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-broker_url)
CELERY_BACKEND | redis://redis:6379/1 | [Docs](https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-result_backend)
CELERY_TIMEZONE | America/New_York | [Docs](https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-timezone)
CELERY_BEAT_SCHEDULE | | [Docs](https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-beat_schedule)

## Discord

Variable | Default | Description
---|---|---
ANNOUNCEMENT_WEBHOOK_URL | None | URL of Discord announcement channel webhook |
BOT_CHANNEL_WEBHOOK_URL | None | URL of Discord bot command channel webhook |
GUILD_ID | 0 | Discord server's Guid ID |
SCRAPE_BOT_TOKEN | None | Discord bot token required by the LFG helper bot |

## Misc

Variable | Default | Description
---|---|---
DOMJUDGE_URL | https://domjudge.cs.fsu.edu/public | Full URL of DOMjudge server. Used for homepage server status card.
HASHID_FIELD_SALT | a long string[^3] | [Docs](https://pypi.org/project/django-hashid-field/)
GTAG | None | [Google Analytics site tag](https://support.google.com/analytics/answer/12002338?hl=en)

[^1]: `Programming-Contest-Suite/src/contestsuite/settings.py`
[^2]: `86@j2=z!=&1r_hoqboog1#*mb$jx=9mf0uw#hrs@lw&7m34sqz`
[^3]: `0s97rx*t4%68jell&lw3^)97o*kr*+*2o^(76q)ix+ilc!4ax#`
