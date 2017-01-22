""" Models containing mainly data from autoscout"""

from django.db import models

class AutoscootData(models.Model):
    """ Shared information of all autoscout models """

    item_id = models.CharField(max_length=120)
    description = models.CharField(max_length=120)

    def __str__(self):
        return '{item_id}: {description}'.format(**self.__dict__)

    class Meta:
        abstract = True

class Brands(AutoscootData):
    """ The Brands of the cars"""

class Equipments(AutoscootData):
    """ The Brands of the cars"""

class Fuel(AutoscootData):
    """ Type of fuel """

class Gear(AutoscootData):
    """ Type of Gear """

class Color(AutoscootData):
    """ Type of Color """

class Painting(AutoscootData):
    """ Type of Painting """

class Body(AutoscootData):
    """ Type of Body """

class Category(AutoscootData):
    """ Type of Usage """
