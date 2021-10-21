#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput
python3 manage.py initadmin
python3 manage.py runserver 0.0.0.0:8000