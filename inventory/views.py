# pylint: disable=no-self-use
""" Views for Inventory"""


from django.shortcuts import render
from django.http.response import Http404

from inventory import services


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

def vehicles_grid(request):
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
    return render(request, 'inventory/grid_cars.html', context)

def vehicle_details(request, vehicle_id):
    """ Return the detail of a vehicle """
    autoscout = services.AS24WSSearch()
    vehicles = autoscout.list_vehicles()
    try:
        vehicle = autoscout.details_vehicle(vehicle_id)
    except IndexError:
        raise Http404('The page does not exists')

    uri_images_big = autoscout.uri_images('big')
    uri_images_main = autoscout.uri_images('main')
    uri_images_thumb = autoscout.uri_images('thumb')
    context = {\
        'vehicle': vehicle,
        'vehicles': vehicles,
        'uri_images_big': uri_images_big,
        'uri_images_thumb': uri_images_thumb,
        'uri_images_main': uri_images_main\
    }
    return render(request, 'inventory/details_car.html', context)

def reprises(request):
    """ Return the html reprises """
    return render(request, 'inventory/reprises.html')

def inspection(request):
    """ Return the html inspection """
    return render(request, 'inventory/inspection.html')

def contact(request):
    """ Return the contact """
    return render(request, 'inventory/contact.html')

def horaire(request):
    """ Return horaire """
    return render(request, 'inventory/horaire.html')
