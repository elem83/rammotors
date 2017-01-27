#!/bin/bash

# git fetch --all
# git reset --hard origin/master
git pull origin master
./manage.py collectstatic --noinput
./manage.py makemigrations
./manage.py migrate
python manage.py get_enumerations
../apache2/bin/restart
