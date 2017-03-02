""" Retrieve lookup value from Autocout24 """
from django.core.management.base import BaseCommand

from inventory.models import Enumeration
from inventory.services import AS24WSSearch

class Command(BaseCommand):
    """ Retrieve enumeration from Autoscout24 """
    help = 'Retrieve enumeration from Autoscout24'

    def handle(self, *args, **options):
        """ Mandatory method """
        Enumeration.objects.all().delete()
        for elem in AS24WSSearch().get_lookup_data():
            Enumeration.objects.create(**elem)
