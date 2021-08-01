FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # Dependencies for building Python packages
  && apt-get install -y build-essential \
  # Translations dependencies
  && apt-get install -y gettext \
  # MariaDB dependency
  && apt-get install -y libmariadb-dev \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Requirements are installed here to ensure they will be cached.
RUN pip install --upgrade pip
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./src app

WORKDIR /app/

COPY ./deploy/contestsuite/scripts/django/start.sh start
RUN sed -i 's/\r$//g' start
RUN chmod +x start

COPY ./deploy/contestsuite/scripts/celery/worker/start.sh start-celeryworker
RUN sed -i 's/\r$//g' start-celeryworker
RUN chmod +x start-celeryworker
