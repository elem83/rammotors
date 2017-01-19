""" Views for Inventory"""
from django.shortcuts import render

# Create your views here.

def vehicules_list(request):
    return render(request, 'inventory/list_cars.html')
