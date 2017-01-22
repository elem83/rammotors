""" Importing all the codes from autoscout

This script can be tested in Django with ipython:
        python manage.py shell
        %run scripts/database.py

    Then save the data file in csv, ideally in data.
"""


import csv
import os
import sys

import django

sys.path.append('.')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rammotors.settings")
django.setup()

from inventory import models

def upload_csv():
    """ Upload the data

    Input:
        file :: String
        path to the file containing the data in csv

    Returns:
        Nothing

    Side Effect:
        build the database Brands
    """
    brands = 'data/brands.csv'
    equipments = 'data/equipments.csv'
    body = 'data/body.csv'
    color = 'data/colors.csv'
    fuel = 'data/fuel.csv'
    gear = 'data/gear.csv'
    painting = 'data/painting.csv'
    category = 'data/categories.csv'

    with open(brands) as fh_brands:
        reader = csv.reader(fh_brands)
        next(reader, None) # Remove header
        for row in reader:
            models.Brands.objects.get_or_create(item_id=row[0], description=row[1])

    with open(equipments) as fh_file:
        reader = csv.reader(fh_file)
        next(reader, None) # Remove header
        for row in reader:
            models.Equipments.objects.get_or_create(item_id=row[0], description=row[1])

    with open(body) as fh_file:
        reader = csv.reader(fh_file)
        next(reader, None) # Remove header
        for row in reader:
            models.Body.objects.get_or_create(item_id=row[0], description=row[1])

    with open(color) as fh_file:
        reader = csv.reader(fh_file)
        next(reader, None) # Remove header
        for row in reader:
            models.Color.objects.get_or_create(item_id=row[0], description=row[1])

    with open(fuel) as fh_file:
        reader = csv.reader(fh_file)
        next(reader, None) # Remove header
        for row in reader:
            models.Fuel.objects.get_or_create(item_id=row[0], description=row[1])

    with open(gear) as fh_file:
        reader = csv.reader(fh_file)
        next(reader, None) # Remove header
        for row in reader:
            models.Gear.objects.get_or_create(item_id=row[0], description=row[1])

    with open(painting) as fh_file:
        reader = csv.reader(fh_file)
        next(reader, None) # Remove header
        for row in reader:
            models.Painting.objects.get_or_create(item_id=row[0], description=row[1])

    with open(category) as fh_file:
        reader = csv.reader(fh_file)
        next(reader, None) # Remove header
        for row in reader:
            models.Category.objects.get_or_create(item_id=row[0], description=row[1])

if __name__ == '__main__':
    upload_csv()
