#!/usr/bin/env bash
exec gunicorn --chdir app  -b :5000 flask-api:app