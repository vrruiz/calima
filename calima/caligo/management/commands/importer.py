# -*- coding: utf-8 -*-
##
## calima - Importa los datos en bruto a la base de datos
##
## $ python manage.py importer <directorio> <año 1> <año 2> ...
##

from django.core.management.base import BaseCommand, CommandError
from caligo.models import station_importer
from parser import Calima

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
        station_importer(calima.estaciones)


