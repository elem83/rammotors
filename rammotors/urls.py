"""rammotors URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from inventory import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.vehicles_list, name='vehicles_list'),
    url(r'^list/$', views.vehicles_list, name='vehicle_list'),
    url(r'^grid/$', views.vehicles_grid, name='vehicle_grid'),
    url(r'^iso/$', views.iso, name='iso'),
    url(r'^car/(\d+)$', views.vehicle_details, name='vehicle_details'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
