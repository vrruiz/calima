# -*- coding: utf-8 -*-
##
## calima - Procesador de datos en bruto a clases Python
## 

from ftplib import FTP
import sys, os, datetime
import re, glob, gzip, csv
from decimal import Decimal, InvalidOperation

FTP_URL = 'ftpdatos.aemet.es'

import logging
logger = logging.getLogger('calima')
hdlr = logging.FileHandler('error.log')
logger.addHandler(hdlr) 

class Calima(object):
    def __init__(self, ftp=FTP_URL, path='./'):
        """
            Genera la estructura Estaciones desde el directorio  datos
            descargados

        """
        self.ftp = ftp
        self.path = path
        self.estaciones = {}

    def generarEstaciones(self):
        try:
            f = open(os.path.join(self.path, 'maestro.csv'), 'r')
        except IOError:
            raise Exception("File not found")
            return

        self.estaciones = {}
        for x in csv.reader(f.readlines()[1:], delimiter=';'):
            self.estaciones[x[0]] = Estacion(x[0], x[1], x[2], x[3], x[4], x[5])

        f.close()

    def _importarEstacion(self, estacionId):
        if not estacionId in self.estaciones:
            raise Exception("Identificacion de estacion invalido")
            return

        # XXX Funciona, pero usarmoe generarDatosAnual
        f = gzip.open(os.path.join(self.path, 'valores_diarios/estacion/%s.CSV.gz' % estacionId))
        self.estaciones[estacionId].cargarDiarios(csv.reader(f.readlines()[1:],
                delimiter=';'))
        f.close()

    def getEstacion(self, estacionId):
        return self.estaciones[estacionId]

    def generarDatosEstacion(self, estacionId=None):
        if not self.estaciones:
            self.generarEstaciones()

        if not estacionId:
            [self._importarEstacion(x) for x in self.estaciones.keys()]

    def _importarAnual(self, year):
        if not self.estaciones:
            self.generarEstaciones()

        logger.info("Extrayendo datos de %d" % year)
        try:
            f = gzip.open(os.path.join(self.path, '%d.CSV.gz' % year))
        except:
            raise Exception("No se pueden cargar datos para el anho %s" % year)

        for dato in csv.reader(f.readlines()[1:], delimiter=';'):
            self.estaciones[dato[0]].cargarParte(dato)

        f.close()

    def generarDatosAnual(self, year=None):
        """ Generar datos dado un ano (year)

            year: integer o iterable de integers, cargar valores para ese dia
                en caso de ser None, carga todos los valores para los 
                ficheros datos
        """
        if not year:
            for file in glob.glob(os.path.join(self.path,'????.CSV.gz')):
                year = re.search('(?P<year>\d\d\d\d).CSV.gz',
                        file).groupdict()['year']
                self._importarAnual(int(year))
            return

        try:
            iterator = iter(year)
        except:
            self._importarAnual(year)
        else:
            for year in year:
                self._importarAnual(year)

    def actualizar(self):
        """ 
            Descarga el fichero para el ultimo anho y maestro.csv en path
            parsear los datos
        """
        ano = datetime.datetime.today().year
        f = "%d.CSV.gz" % ano
        # Inicia sesión FTP
        ftp = FTP(self.ftp)
        ftp.login()
        # Ir a series climatológicas
        ftp.cwd('series_climatologicas')
        ftp.retrbinary('RETR maestro.csv', open(os.path.join(self.path, 'maestro.csv'), 'wb').write)
        ftp.cwd('valores_diarios')
        ftp.cwd('anual')
        try:
            ftp.retrbinary('RETR ' + f, open(os.path.join(self.path, f), 'wb').write)
        except:
            os.remove(f)

        ftp.quit()
        
        # Parsear los datos
        self._importarAnual(ano)


# TODO Dar valor a Acum si queremos que quede reflejado db
ESPECIALES = {'Ip': 'Ip', 'Acum': None, 'Varias': None, '': None}

def exceptionEspeciales(f):
    def new_f(value):
        try:
            return f(value)
        except (ValueError, InvalidOperation):
            # Valores especiales
            if value in ESPECIALES:
                return ESPECIALES[value] 
            else:
                logger.error('Improper value parsing file, val: %s %s' % (str(value),
                        str(sys.exc_info())))
                return None
    new_f.__name__ = f.__name__
    return new_f

def floatES(d):
    # faster than waiting for exception
    if not d:
        return  None
    try:
        return Decimal(d.replace(',','.'))
    except InvalidOperation:
        return ESPECIALES[d] 

@exceptionEspeciales
def hora_min(h):
    if not h:
        return None 
    hora, minutos = h.split(':')
    return datetime.time(int(hora), int(minutos))

@exceptionEspeciales
def hora(h):
    if not h:
        return None 
    h_int = int(h)
    return h_int>23 and datetime.time(23) or datetime.time(h_int)



class Estacion(object):
    def __init__(self, id, nombre, provincia, altitud, latitud, longitud):
        self.id = id
        self.nombre = nombre
        self.provincia = provincia
        self.altitud = int(altitud)
        # Introduce un punto decimal que no está en la documentación
        # 410653N 012439W -> 41.0653 -1.2439
        latitud = latitud[:2] + '.' + latitud[2:]
        longitud = longitud[:2] + '.' + longitud[2:]
        if latitud[-1] == 'S':
            self.latitud = -1 * Decimal(latitud[:-1])
        else:
            self.latitud = Decimal(latitud[:-1])
        if longitud[-1] == 'W':
            self.longitud = -1 * Decimal(longitud[:-1])
        else:
            self.longitud = Decimal(longitud[:-1])
        self.valores = {}

    def __repr__(self):
        return "<%s: %s>" % (self.id, self.nombre)

    def valoresDiarios(self, fecha):
        pass

    def cargarParte(self, d):
        fecha = datetime.date(int(d[4]),int(d[5]),int(d[6]))
        #for i in range(len(d)):
        #    print "%s : %s" % (i, d[i])
        self.valores[fecha] = {
                't_max' : (floatES(d[7]), hora_min(d[8])),
                't_min' : (floatES(d[9]), hora_min(d[10])),
                't_med' : floatES(d[11]),
                'racha' : (floatES(d[12]), floatES(d[13]), hora_min(d[14])),
                'vel_media': floatES(d[15]),
                'prec' : floatES(d[16]),
                'sol' : floatES(d[17]),
                'max_press': (floatES(d[18]), hora(d[19])),
                'min_press': (floatES(d[20]), hora(d[21]))
            }

    def cargarDiarios(self, datos):
        """ datos """
        for d in datos:
            self.cargarParte(d)

if __name__ == "__main__":
    calima = Calima(path='../../../../data/datos/')
    calima.generarEstaciones()
    #calima.actualizar()
    calima.generarDatosAnual([2010])
    #print calima.estaciones.keys()
    #print "Numero estaciones ", len(calima.estaciones)
    #calima.generarDatosAnual([2009,2010])
    #calima.generarDatosAnual(2009)
    #calima.generarDatosAnual(2012)
    #print [calima.getEstacion(x).valores for x in calima.estaciones]
    #estacion = calima.estaciones['8500A']
    #print estacion.provincia

