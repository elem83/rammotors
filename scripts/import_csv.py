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

def upload_brands():
    """ Upload the brands

    Input:
        file :: String
        path to the file containing the data in csv

    Returns:
        Nothing

    Side Effect:
        build the database Brands
    """
    brands = 'data/brands.csv'
    with open(brands) as fh_brands:
        reader = csv.reader(fh_brands)
        next(reader, None) # Remove header
        for row in reader:
            models.Brands.objects.get_or_create(brand_id=row[0], description=row[1])


if __name__ == '__main__':
    upload_brands()
