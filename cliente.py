from ftplib import FTP
import os, datetime
import glob, gzip, csv
import re
import sys

FTP=''

import logging
logger = logging.getLogger('calima')
hdlr = logging.FileHandler('error.log')
logger.addHandler(hdlr) 

class Calima(object):
    def __init__(self, ftp=FTP, path='./'):
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

        # old: valores_diarios/estacion/
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

        try:
            f = gzip.open(os.path.join(self.path, '%d.CSV.gz' % year))
        except:
            raise Exception("No se pueden cargar datos para el anho %s" % year)

        for dato in csv.reader(f.readlines()[1:], delimiter=';'):
            self.estaciones[dato[0]].cargarParte(dato)

        f.close()

    def generarDatosAnual(self, year=None):
        """ Generar datos dado un anho (year)

            year: integer o iterable, cargar valores para ese dia
                en caso de ser None, carga todos los valores para los 
                ficheros datos
        """
        if not year:
            for file in glob.glob(os.path.join(self.path,'????.CSV.gz')):
                year = re.search('(?P<year>\d\d\d\d).CSV.gz',
                        file).groupdict()['year']
                self._importarAnual(year)
            return

        try:
            iterator = iter(year)
        except:
            self._importarAnual(year)
        else:
            for year in year:
                self._importarAnual(year)


ESPECIALES = {'Ip': 'Ip', 'Acum': 'Acum', 'Varias': 'Varias', '': None}

def exceptionEspeciales(f):
    def new_f(value):
        try:
            return f(value)
        except ValueError:
            # Valores especiales
            if value in ESPECIALES:
                return ESPECIALES[value] 
            else:
                logger.error('Improper value parsing file %s %s' % (str(value),
                        str(sys.exc_info())))
                #raise Exception('Error parsing line')
                return value
    new_f.__name__ = f.__name__
    return new_f

    
class Estacion(object):
    def __init__(self, id, nombre, provincia, altitud, latitud, longitud):
        self.id = id
        self.nombre = nombre
        self.provincia = provincia
        self.altitud = int(altitud)
        if altitud[-1] == 'S':
            self.latitud = -1 * int(latitud[:-1])
        if longitud[-1] == 'W':
            self.longitud = -1 * int(longitud[:-1])
        self.valores = {}

    def __repr__(self):
        return "<%s: %s>" % (self.id, self.nombre)

    def valoresDiarios(self, fecha):
        pass

    def cargarParte(self, d):
        @exceptionEspeciales
        def floatES(d):
            return float(d.replace(',','.'))

        @exceptionEspeciales
        def hora(h):
            hora, minutos = h.split(':')
            return datetime.time(int(hora), int(minutos))

        fecha = datetime.date(int(d[4]),int(d[5]),int(d[6]))
        #for i in range(len(d)):
        #    print "%s : %s" % (i, d[i])
        self.valores[fecha] = {
                't_max' : (floatES(d[7]), hora(d[8])),
                't_min' : (floatES(d[9]), hora(d[10])),
                't_med' : floatES(d[11]),
                'racha' : (floatES(d[12]), floatES(d[13]), hora(d[14])),
                'vel_media': floatES(d[15]),
                'prec' : floatES(d[16]),
                'sol' : floatES(d[17]),
                'pres_max': (floatES(d[18]), floatES(d[19])),
                'prex_min': (floatES(d[20]), floatES(d[21]))
            }

    def cargarDiarios(self, datos):
        """ datos """
        for d in datos:
            self.cargarParte(d)

if __name__ == "__main__":
    calima = Calima(path='datos/')
    calima.generarEstaciones()
    print calima.estaciones.keys()
    print "Numero estaciones ", len(calima.estaciones)
    #calima.generarDatosAnual([2009,2010])
    calima.generarDatosAnual(2009)
    #calima.generarDatosAnual(2012)
    #print [calima.getEstacion(x).valores for x in calima.estaciones]
    print calima.estaciones[calima.estaciones.keys()[0]].valores

