""" Views for Inventory"""


from django.shortcuts import render

from inventory import services

# Create your views here.


def vehicles_list(request):
    """ Return the context and render templates """
    autoscout = services.AS24WSSearch()
    images_uri = autoscout.uri_images('main')
    vehicles = autoscout.list_vehicles()
    brands = services.filter_brands(vehicles)
    context = {\
        'vehicles': vehicles,
        'images_uri': images_uri,
        'brands': brands\
    }
    return render(request, 'inventory/list_cars.html', context)

def vehicle_details(request):
    """ Return the detail of a vehicle """
    autoscout = services.AS24WSSearch()
    vehicle = autoscout.details_vehicle(304915410)
    uri_images_big = autoscout.uri_images('big')
    uri_images_main = autoscout.uri_images('main')
    uri_images_thumb = autoscout.uri_images('thumb')
    vehicles = autoscout.list_vehicles()
    context = {\
        'vehicle': vehicle,
        'vehicles': vehicles,
        'uri_images_big': uri_images_big,
        'uri_images_thumb': uri_images_thumb,
        'uri_images_main': uri_images_main\
    }
    return render(request, 'inventory/details_car.html', context)

