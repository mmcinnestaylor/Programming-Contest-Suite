FROM python:3.9-slim
LABEL maintainer="ACM at FSU <contestdev@fsu.acm.org>"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ARG REQUIREMENTS=requirements.txt

RUN apt-get update \
  # Dependencies for building Python packages
  && apt-get install -y --no-install-recommends build-essential \
  # Translations dependencies
  && apt-get install -y gettext \
  # MariaDB dependency
  && apt-get install -y libmariadb-dev \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Requirements are installed here to ensure they will be cached.
RUN pip install --upgrade pip
COPY $REQUIREMENTS /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt \
  && rm -rf /tmp/requirements.txt \
  && useradd -U app_user \
  && install -d -m 0755 -o app_user -g app_user /app/static \
  && install -d -m 0755 -o app_user -g app_user /app/media/contest_files \
  && install -d -m 0755 -o app_user -g app_user /app/media/ec_files \
  && install -d -m 0755 -o app_user -g app_user /app/media/uploads

# Code and User Setup
WORKDIR /app

USER app_user:app_user

COPY --chown=app_user:app_user src .
COPY --chown=app_user:app_user deploy/prod/contestsuite/scripts/*.sh docker/

RUN chmod +x docker/*.sh

# Docker Run Checks and Configurations
ENTRYPOINT [ "docker/entrypoint.sh" ]

CMD [ "docker/start.sh", "server" ]
