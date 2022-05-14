#!/bin/bash

cd /app

if [ $# -eq 0 ]; then
    echo "Usage: start.sh [PROCESS_TYPE](server/worker)"
    exit 1
fi

PROCESS_TYPE=$1
MODE=${2:-production}

if [ "$PROCESS_TYPE" = "server" ]; then
    if [ "$MODE" = "debug" ]; then
        python \
            manage.py \
            runserver \
            0.0.0.0:8000
    else
        gunicorn \
            --bind 0.0.0.0:8000 \
            --workers 4 \
            --threads 4 \
            --worker-class gthread \
            --worker-tmp-dir /dev/shm \
            --log-level DEBUG \
            --access-logfile "-" \
            --error-logfile "-" \
            contestsuite.wsgi:application
    fi
elif [ "$PROCESS_TYPE" = "worker" ]; then
    celery \
        -A contestsuite \
        worker \
        --autoscale=10,3 \
        -n worker@%n \
        --loglevel INFO
else
    echo "Invalid [PROCESS_TYPE](server/worker)"
    exit 1
fi
