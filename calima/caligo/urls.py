from django.conf.urls.defaults import patterns, include, url
from caligo import views

filtros = {
    'temperatura/minimo'         : 'min_t',
    'temperatura/maximo'         : 'max_t',
    'viento/racha/maximo'        : 'max_squall',
    'viento/racha/minimo'        : 'min_squall',
    'precipitacion_diaria/maximo': 'max_prec',
    'precipitacion_diaria/minimo': 'min_prec',
}

urlpatterns = patterns('',
    url(r'^provinces/(?P<provinceId>\d+)', views.provinces),
    url(r'^provinces/', views.provinces),

    url(r'^stations/(?P<stationId>\w+)/$', views.stations),
    url(r'^stations/$', views.stations),

    url(r'^stats/', views.stats),

    url(r'^api/', views.api),
    url(r'^about/', views.about),
    url(r'^$', views.index_html),
    url(r'^index.html', views.index_html),
)

for key in filtros:
    urlpatterns.append(url(r'stations/(?P<stationId>\w+)/%s$' % key, views.stations,
            {'filtro': filtros[key]}))
