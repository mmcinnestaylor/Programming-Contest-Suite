---
title: Home
layout: home
nav_order: 1
---

Welcome to the documentation for the Programming Contest Suite (PCS), a set of tools for running [ICPC](https://icpc.global) style programming competitions hosted by the [Association for Computing Machinery Florida State University Student Chapter](https://fsu.acm.org). The suite is designed to work with a [DOMJudge](https://www.domjudge.org/) jury system by facilitating contest registration and management, generating contestant data files required by DOMjudge, and processing contest results.

<span class="fs-5">
    [contest.cs.fsu.edu](https://contest.cs.fsu.edu){: .btn .btn-purple }
    [View on GitHub](https://github.com/mmcinnestaylor/Programming-Contest-Suite){: .btn }
</span>

<hr>

## Installation

Clone the repository: 

	git clone https://github.com/mmcinnestaylor/Programming-Contest-Suite.git


Alternatively, download one of the versions available on the [releases](https://github.com/mmcinnestaylor/Programming-Contest-Suite/releases) page.  

## Deployment

There are many ways to [deploy Django](https://docs.djangoproject.com/en/4.2/howto/deployment/). The project has been extenively tested with and includes files for deploying using [Docker](https://www.docker.com/).

### Docker

Please reference our [Docker image documentation]({{ site.url }}/docker.html) for creation and usage details. Pre-built images are available in the project's [Docker Hub repository](https://hub.docker.com/r/acmfsu/contestsuite). An example deployment intended for [Docker Compose](https://docs.docker.com/compose/) and suitable for local development and testing purposes is available in the repository's [deploy directory](https://github.com/mmcinnestaylor/Programming-Contest-Suite/tree/main/deploy).

#### Default Superuser
user: `contestadmin`  
pass: `seminoles1!`

A default superuser account is created when the container connects to an empty database. The default password should be changed to secure the account.

### Production

The default values of `SECRET_KEY` and `HASHID_FIELD_SALT` are not safe for production use and should be changed. Django secret key generators are readily available online.

### Quick-start

The following steps outline running the PCS outside of a Docker context. This is minimally sufficient for development or internal testing, but not for a production deployment. 

#### Install Project Requirements

```
# Programming-Contest-Suite/

pipenv install
```

#### Spin-up Support Services

Using the default configuration, Django and Celery rely on instances of MariaDB, Redis, and RabbitMQ. Server addresses and credentials should be passed to Django and Celery via envronment variables. 

#### Start Django & Celery 

##### Web Server

```
# Programming-Contest-Suite/src/

gunicorn contestsuite.wsgi:application
```

##### Celery Worker

```
# Programming-Contest-Suite/src/

celery -A contestsuite worker
```

##### Celery Beat

```
# Programming-Contest-Suite/src/

celery -A contestsuite beat --scheduler django_celery_beat.schedulers:DatabaseScheduler
``````

# Contributing

We welcome contributions to the project! Check out the [Contributor's Guide](https://github.com/mmcinnestaylor/Programming-Contest-Suite/blob/main/CONTRIBUTING.md) to learn how to get started.

### Thank you to the contributors of the project!

- [Marlan McInnes-Taylor](https://github.com/mmcinnestaylor) *Creator*
- [Daniel Riley](https://github.com/danielmriley) 
