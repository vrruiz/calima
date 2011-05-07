from django.core.management.base import BaseCommand, CommandError

from cliente import Calima

from caligo.models import Station, Province, DailyReport

class Command(BaseCommand):
    # args es path al directorio con los ficheros anuales
    args = '<directorio> <anho1> <anho2>'
    help = 'Importa los datos de un directorio a la db'

    def handle(self, *args, **options):
        calima = Calima(path=args[0])
        ## Specify the year
        if len(args) > 1:
            calima.generarDatosAnual(map(int, args[1:]))
        else:
            calima.generarDatosAnual()
        for estacion in calima.estaciones.values():
            province, created = Province.objects.get_or_create(
                    name=unicode(estacion.provincia,
                        'iso8859-1').encode('utf8'))
            
            if created:
                print "Created province %s" % province.name

            print "Processing estacion", estacion.altitud, estacion.latitud, estacion.longitud, estacion.id, estacion.nombre
            station, created = Station.objects.get_or_create(code=estacion.id,
                    name=unicode(estacion.nombre, 'iso8859-1').encode('utf8'),
                    province=province,
                    altitude=estacion.altitud,
                    latitude=estacion.latitud,
                    longitude=estacion.longitud)
            if created:
                print "created station %s" % station.name

            for key in estacion.valores:
                datos = estacion.valores[key]
                daily = DailyReport(date=key,
                        station=station,
                        max_t          = datos['t_max'][0],
                        max_t_time     = datos['t_max'][1],
                        min_t          = datos['t_min'][0],
                        min_t_time     = datos['t_min'][1],
                        avg_t          = datos['t_med'],
                        squall         = datos['racha'][0],
                        squall_dir     = datos['racha'][1],
                        squall_time    = datos['racha'][2],
                        wind_avg_speed = datos['vel_media'],
                        # yeah, I know
                        precip         = type(datos['prec']) != str and datos['prec'] or None,
                        sunshine       = datos['sol'],
                        max_press      = datos['max_press'][0],
                        max_press_time = datos['max_press'][1],
                        min_press      = datos['min_press'][0],
                        min_press_time = datos['min_press'][1],
                        imp_prec      = datos['prec'] == 'Ip' and True or False,
                )
                daily.save()
                # TODO
                # si el viento es 99 no he hecho nada.. habra que actualizar
                # campo
                # con Varias el valor queda Nulo, supongo que es correcto


