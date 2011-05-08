from django.conf.urls.defaults import *
from piston.resource import Resource
from calima.api.handlers import ProvinceHandler, StationHandler

province_handler = Resource(ProvinceHandler)
station_handler = Resource(StationHandler)

urlpatterns = patterns('',
    url(r'^province/(?P<name>[^/]+)/', province_handler),
    url(r'^provinces/', province_handler),
    url(r'^station/(?P<code>[^/]+)/', station_handler),
    url(r'^stations/', station_handler),
)