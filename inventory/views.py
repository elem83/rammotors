""" Views for Inventory"""


from django.shortcuts import render

from inventory import services

# Create your views here.


def vehicles_list(request):
    """ Return the context and render templates """
    autoscout = services.WsdlAutoscout24()
    images_uri = autoscout.uri_images('main')
    vehicles = autoscout()
    brands = services.filter_brands(vehicles)
    context = {\
        'vehicles': vehicles,
        'images_uri': images_uri,
        'brands': brands\
    }
    return render(request, 'inventory/list_cars.html', context)

def vehicle_details(request):
    """ Return the detail of a vehicle """
    autoscout = services.WsdlAutoscout24()
    images_uri = autoscout.uri_images('main')
    vehicles = autoscout()
    brands = services.filter_brands(vehicles)
    context = {\
        'vehicle': vehicles[0],
        'vehicles': vehicles,
        'images_uri': images_uri,
        'brands': brands\
    }
    return render(request, 'inventory/details_car.html', context)

