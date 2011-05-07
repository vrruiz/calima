from django.conf.urls.defaults import *
from piston.resource import Resource
from calima.api.handlers import StationHandler

station_handler = Resource(StationHandler)

urlpatterns = patterns('',
   url(r'^station/(?P<code>[^/]+)/', station_handler),
   url(r'^stations/', station_handler),
)