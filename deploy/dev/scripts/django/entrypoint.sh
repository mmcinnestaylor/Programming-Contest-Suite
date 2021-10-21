#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python3 /app/manage.py migrate --noinput
python3 /app/manage.py collectstatic --noinput
python3 /app/manage.py initadmin
python3 /app/manage.py runserver 0.0.0.0:8000