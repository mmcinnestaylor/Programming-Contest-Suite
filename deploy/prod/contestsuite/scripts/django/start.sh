#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput
python3 manage.py initadmin
gunicorn contestsuite.wsgi:application --bind 0.0.0.0:8000 --workers=4 --threads=4 --worker-class=gthread --worker-tmp-dir /dev/shm --log-file=-
