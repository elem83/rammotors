""" Views for Inventory"""
from django.shortcuts import render

from inventory import services

# Create your views here.

def vehicules_list(request):
    autoscout = services.WsdlAutoscout24()
    images_uri = autoscout.uri_images('main')
    vehicles = autoscout()
    context = {'vehicles': vehicles, 'images_uri': images_uri}
    return render(request, 'inventory/list_cars.html', context)
