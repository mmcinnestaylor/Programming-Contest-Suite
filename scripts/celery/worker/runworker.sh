#!/bin/bash

export DEBUG=True
exec celery -A ../../src/contestsuite worker -l INFO
