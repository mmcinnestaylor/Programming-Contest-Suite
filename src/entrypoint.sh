#!/bin/bash

# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# fail exit if one of your pipe command fails
set -o pipefail
# exits if any of your variables is not set
set -o nounset

mariadb_ready() {
python << END

from mariadb import connect, OperationalError
from sys import exit

try:
    connect(
        dbname="${SQL_DATABASE}",
        user="${SQL_USER}",
        password="${SQL_PASSWORD}",
        host="${SQL_HOST}",
        port="${SQL_PORT}",
    )
except OperationalError:
    exit(-1)
exit(0)

END
}
until mariadb_ready; do
  >&2 echo 'Waiting for MariaDB to become available...'
  sleep 1
done
>&2 echo 'MariaDB is available'

exec "$@"