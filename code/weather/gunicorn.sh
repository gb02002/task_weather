#!/bin/bash

gunicorn -c ./gunicorn.config.py 'orgproj.wsgi:application'


