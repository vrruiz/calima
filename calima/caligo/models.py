# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Province(models.Model):
    """A Spanish province"""

    name = models.CharField(_(u'name'), max_length=100)

    def __unicode__(self):
        return self.name


class Station(models.Model):
    """A meteorological station"""

    code = models.CharField(verbose_name=_(u'Climatologic code'), max_length=10)
    syn_code = models.PositiveIntegerField(verbose_name=_(u'Synoptic code'), blank=True, null=True)
    name = models.CharField(verbose_name=_(u'Name'), max_length=100)
    province = models.ForeignKey("Province", verbose_name=_(u'Province to which this station \
        belongs'), related_name='stations', blank=True, null=True)
    altitude = models.IntegerField(verbose_name=_(u'Altitude (m)'), blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True, editable=False)
    longitude = models.FloatField(blank=True, null=True, editable=False)

    def __unicode__(self):
        return "%s: %s" % (self.code, self.name)


class DailyReport(models.Model):
    """A daily meteorological report"""

    date = models.DateTimeField(_('Date'), null=False)
    station = models.ForeignKey("Station", verbose_name=_(u'Station to which this report applies'),
        related_name='reports', blank=True, null=True)
    max_t = models.DecimalField(verbose_name=_(u'Maximum temperature (ºC)'), max_digits=5,
        decimal_places=2, blank=True, null=True)
    max_t_time = models.TimeField(verbose_name=_(u'Time of maximum temperature'), blank=True,
    	null=True)
    min_t = models.DecimalField(verbose_name=_(u'Minimum temperature (ºC)'), max_digits=5,
        decimal_places=2, blank=True, null=True)
    min_t_time = models.TimeField(verbose_name=_(u'Time of minimum temperature'), blank=True,
    	null=True)
    avg_t = models.DecimalField(verbose_name=_(u'Average temperature (ºC)'), max_digits=5,
        decimal_places=2, blank=True, null=True)
    squall = models.DecimalField(verbose_name=_(u'Maximum squall (m/s)'),
            max_digits=7, decimal_places=2, blank=True, null=True)
    squall_dir = models.IntegerField(verbose_name=_(u'Direction of maximum squall (degrees*10)'),
    	blank=True, null=True)
    squall_time = models.TimeField(verbose_name=_(u'Time of maximum squall'), blank=True,
    	null=True)
    wind_avg_speed = models.DecimalField(verbose_name=_(u'Average wind speed (m/s)'), max_digits=7,
    	decimal_places=2, blank=True, null=True)
    precip = models.DecimalField(verbose_name=_(u'Precipitaion (mm)'),
            max_digits=7,
        decimal_places=2, blank=True, null=True)
    sunshine = models.DecimalField(verbose_name=_(u'Sunshine (hours)'),
            max_digits=7,
        decimal_places=2, blank=True, null=True)
    max_press = models.DecimalField(verbose_name=_(u'Maximum barometric pressure (hPa)'),
    	max_digits=7, decimal_places=2, blank=True, null=True)
    max_press_time = models.TimeField(verbose_name=_(u'Time of maximum pressure'), blank=True,
    	null=True)
    min_press = models.DecimalField(verbose_name=_(u'Minimum barometric pressure (hPa)'),
    	max_digits=7, decimal_places=2, blank=True, null=True)
    min_press_time = models.TimeField(verbose_name=_(u'Time of minimum pressure'), blank=True,
        null=True)
    imp_prec = models.BooleanField(verbose_name=_(u'Imperceptible precipitation'))
    var_w_dir = models.BooleanField(verbose_name=_(u'Variable wind direction'))


def station_importer(estaciones):
    """
        Imports the data from a dictionary of station objects as defined in
        the parser.py file
    """
    for estacion in estaciones.values():
        province, created = Province.objects.get_or_create(
                name=unicode(estacion.provincia,
                    'iso8859-1').encode('utf8'))
        
        if created:
            print "Created province %s" % province.name

        print "Processing estacion", estacion.altitud, estacion.latitud, estacion.longitud, estacion.id, estacion.nombre
        station, created = Station.objects.get_or_create(code=estacion.id,
                defaults={
                'name'      : unicode(estacion.nombre, 'iso8859-1').encode('utf8'),
                'province'  : province,
                'altitude'  : estacion.altitud,
                'latitude'  : estacion.latitud,
                'longitude' : estacion.longitud})
        if created:
            print "Created station %s" % station.name

        for key in estacion.valores:
            datos = estacion.valores[key]
            obj, created = DailyReport.objects.get_or_create(
                date=key, station=station, defaults={
                    'max_t'          : datos['t_max'][0],
                    'max_t_time'     : datos['t_max'][1],
                    'min_t'          : datos['t_min'][0],
                    'min_t_time'     : datos['t_min'][1],
                    'avg_t'          : datos['t_med'],
                    'squall'         : datos['racha'][0],
                    'squall_dir'     : datos['racha'][1],
                    'squall_time'    : datos['racha'][2],
                    'wind_avg_speed' : datos['vel_media'],
                    'precip'         : type(datos['prec']) != str and datos['prec'] or None,
                    'sunshine'       : datos['sol'],
                    'max_press'      : datos['max_press'][0],
                    'max_press_time' : datos['max_press'][1],
                    'min_press'      : datos['min_press'][0],
                    'min_press_time' : datos['min_press'][1],
                    'imp_prec'       : datos['prec'] == 'Ip' and True or False,
                }
            )

            # TODO
            # si el viento es 99 no he hecho nada.. habra que actualizar
            # campo
            # con Varias el valor queda Nulo, supongo que es correcto


