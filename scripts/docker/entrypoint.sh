#!/bin/bash

# Bash options
set -o errexit
set -o pipefail
set -o nounset

# Idempotent Django commands
python manage.py migrate --noinput

exec "$@"
