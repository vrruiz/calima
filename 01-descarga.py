#!/usr/bin/python
# -*- coding: utf-8 -*-

##
## calima - Series climatológicas de la AEMET
## Descargar datos del FTP
##

import os
from ftplib import FTP

FTP_AEMET = 'ftpdatos.aemet.es'
DATA_DIR = 'datos'

class Download:
    """ Descarga de datos de la AEMET """

    def __init__(self, url = ''):
        """ Inicialización """
        if (url):
            self.FTP_URL = url
        else:
            self.FTP_URL = FTP_AEMET
        # Cambiar directorio
        self.old_path = os.getcwd()
        # Si no existe el directorio, crearlo
        if not os.path.exists(DATA_DIR):
            os.mkdir(DATA_DIR)
        os.chdir(DATA_DIR)

    def start(self):
        """ Descarga los datos de AEMET en DATA_DIR """
        # Inicia sesión FTP
        ftp = FTP(FTP_AEMET)
        ftp.login()
        # Ir a series climatológicas
        ftp.cwd('series_climatologicas')
        # Descarga maestro.csv
        print "Descargando maestro.csv..."
        ftp.retrbinary('RETR maestro.csv', open('maestro.csv', 'wb').write)
        ftp.cwd('valores_diarios')
        ftp.cwd('anual')
        # Descarga de ficheros
        for f in ftp.nlst():
            if f in "..":
                continue
            print "Descargando %s..." % (f)
            try:
                ftp.retrbinary('RETR ' + f, open(f, 'wb').write)
            except:
                os.remove(f)
                pass

    def __del__(self):
        # Volver al directorio original
        os.chdir(self.old_path)

if (__name__ == '__main__'):
    download = Download()
    download.start()
