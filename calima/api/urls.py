from django.conf.urls.defaults import *
from piston.resource import Resource
from calima.api.handlers import ProvinceHandler, StationHandler, DailyReportHandler

province_handler = Resource(ProvinceHandler)
station_handler = Resource(StationHandler)
report_handler = Resource(DailyReportHandler)

urlpatterns = patterns('',
    url(r'^provincia/$', province_handler),
    url(r'^provincia/(?P<name>[^/]+)/$', province_handler),
    url(r'^estacion/$', station_handler),
    url(r'^estacion/(?P<station_code>[^/]+)/$', station_handler),
    url(r'^estacion/(?P<station_code>[^/]+)/serie/$', report_handler),

)