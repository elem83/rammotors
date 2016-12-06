""" Views for Inventory"""
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def vehicules(request):
    return HttpResponse('<html><title>Vehicules</title></html>')
