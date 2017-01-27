""" Models containing mainly data from autoscout"""

from django.db import models

class Enumeration(models.Model):
    """ List of enumeration in french """

    name = models.CharField(max_length=120)
    item_id = models.CharField(max_length=120)
    text = models.CharField(max_length=120)

    def __str__(self):
        return '{name} ({item_id}): {text}'.format(**self.__dict__)
