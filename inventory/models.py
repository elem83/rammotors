""" Models containing mainly data from autoscout"""

from django.db import models

class Brands(models.Model):
    """ The Brands of the cars"""
    brand_id = models.IntegerField()
    description = models.CharField(max_length=60)

    def __str__(self):
        return '{brand_id}: {description}'.format(**self.__dict__)
