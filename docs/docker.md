---
title: Docker Image
layout: default
---

# Docker Image

The project's `Dockerfile` is designed to build both the development and production versions of the project's Docker Image. 

## Build Image

```
# Programming-Contet-Suite/

docker build . -t <image_name> --build-arg="REQUIREMENTS=requirements.txt"
```

`Dockerfile` Argument | Default | Description
---|---|---
REQUIREMENTS | requirements.txt | Path to the manifest file to use during image creation.

## Run Image

The `Dockerfile` specifies an image capable of running the Django web app, Celery, or a helper Discord bot. The parameters passed to the image's start script `start.sh` determine the container's behavior.

    docker run <image_name> /docker/start.sh <PROCESS_TYPE> <MODE>

`PROCESS_TYPE` | Default | Usage
---|---|---
server | Yes | WSGI server bound to the Django web app
worker | No | Celery Worker
beat | No | Celery Beat
flower | No | Celery Flower
bot | No | Discord bot

`MODE` | Default | Usage
---|---|---
production | Yes | Option specified by `PROCESS_TYPE` uses production ready settings/flags.
debug | No | Option specified by `PROCESS_TYPE` uses debug/development settings/flags.
