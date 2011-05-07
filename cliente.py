import csv
import os
from ftplib import FTP
import glob
import gzip
import re
import datetime

FTP=''

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
        fecha = datetime.date(int(d[4]),int(d[5]),int(d[6]))
        self.valores[fecha] = tuple(d[7:])

    def cargarDiarios(self, datos):
        """ datos """
        for d in datos:
            fecha = datetime.date(int(d[4]),int(d[5]),int(d[6]))
            self.valores[fecha] = tuple(d[7:])

if __name__ == "__main__":
    calima = Calima(path='datos/')
    calima.generarEstaciones()
    print calima.estaciones.keys()
    print "Numero estaciones ", len(calima.estaciones)
    calima.generarDatosAnual([2009,2010])
    calima.generarDatosAnual(2010)
    calima.generarDatosAnual(2012)
    #print [calima.getEstacion(x).valores for x in calima.estaciones]

