""" Views for Inventory"""
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def vehicules_list(request):
    return HttpResponse('<html><title>Ram Motors</title></html>')
