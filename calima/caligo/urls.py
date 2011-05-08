from django.conf.urls.defaults import patterns, include, url
from caligo import views

filtros = {
    'temperatura/minimo'         : 'min_t',
    'temperatura/media'          : 'avg_t',
    'temperatura/maximo'         : 'max_t',
    'viento/direcction'          : 'max_t',
    'viento/direcction/media'    : 'max_t',
    'viento/racha/maximo'        : 'squall',
    'viento/racha/minimo'        : 'max_t',
    'viento/velocidad_media'     : 'wind_avg_speed',
    'precipitacion_diaria/'      : 'max_t',
    'precipitacion_diaria/maximo': 'max_t',
    'precipitacion_diaria/minimo': 'max_t',
}
urlpatterns = patterns('',
    url(r'^provinces/(?P<provinceId>\d+)', views.provinces),
    url(r'^provinces/', views.provinces),

    url(r'^stations/(?P<stationId>\w+)/$', views.stations),
    url(r'^stations/$', views.stations),

    url(r'^api/', views.api),
    url(r'^about/', views.about),
    url(r'^$', views.index_html),
    url(r'^index.html', views.index_html),
)

for key in filtros:
    urlpatterns.append(url(r'stations/(?P<stationId>\w+)/%s$' % key, views.stations,
            {'filtro': filtros[key]}))
