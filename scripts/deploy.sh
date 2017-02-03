#!/bin/bash

# git fetch --all
# git reset --hard origin/master
git pull origin master
./manage.py collectstatic --noinput  --settings=rammotors.settings.staging
./manage.py makemigrations --settings=rammotors.settings.staging
./manage.py migrate --settings=rammotors.settings.staging
python manage.py get_enumerations --settings=rammotors.settings.staging
../apache2/bin/restart
