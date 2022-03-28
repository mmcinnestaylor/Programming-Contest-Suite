#!/bin/bash

export DEBUG=True
exec python3 ../../../../src/manage.py runserver localhost:8000
