#!/bin/bash

# git fetch --all
# git reset --hard origin/master
git pull origin master
./manage.py collectstatic --noinput
./manage.py makemigrations
./manage.py migrate
python scripts/import_csv.py
../apache2/bin/restart
