#!/bin/bash

set -o errexit
set -o nounset

celery -A contestsuite worker --autoscale=10,3 -n worker@%n -l INFO
