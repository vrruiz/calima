from django.conf.urls.defaults import patterns, include, url
from caligo import views

urlpatterns = patterns('',
    url(r'^provinces/(?P<provinceId>\d+)', views.provinces),
    url(r'^provinces/', views.provinces),
)
