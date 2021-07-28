#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput
python3 manage.py initadmin
gunicorn contestsuite.wsgi:application --bind 0.0.0.0:8000