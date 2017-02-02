""" Views for Inventory"""

from collections import defaultdict

from django.shortcuts import render

from inventory import services

# Create your views here.

def filter_brands(vehicles):
    """ Group the cars by brands """
    brands = defaultdict(int)
    for vhc in vehicles:
        brands[vhc.brand] += 1
    return dict(brands)

def vehicules_list(request):
    """ Return the context and render templates """
    autoscout = services.WsdlAutoscout24()
    images_uri = autoscout.uri_images('main')
    vehicles = autoscout()
    brands = filter_brands(vehicles)
    context = {\
        'vehicles': vehicles,
        'images_uri': images_uri,
        'brands': brands\
    }
    return render(request, 'inventory/list_cars.html', context)
