# -*- coding: utf-8 -*-
##
## calima - Genera un gráfico de información con el histórico de datos
##
## $ python manage.py infographic <fichero.png>
##
import calendar

from PIL import Image, ImageDraw, ImageFont

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Avg, Max, Min, Count
from caligo.models import DailyReport, Station
from color_scheme import scheme

PIX_SIZE = 25
TEMP_MIN = -15
TEMP_MAX = 45
COLOR_WEIGHT = 256.0 / (TEMP_MAX + abs(TEMP_MIN) + 1)
FONT = '/Library/Fonts/Arial.ttf' # TODO: Find font path
FONT_SIZE = 20
MARGIN_FONT = 10
LOGO_IMAGE='/Users/rvr/archivos/prog/abredatos/calima/calima/caligo/static/images/calima-300x76.png' # TODO: Relative path

MONTHS = [
    ['Enero', 31], ['Febrero', 28], ['Marzo', 31], ['Abril', 30], ['Mayo', 31],
    ['Junio', 30], ['Julio', 31], ['Agosto', 31], ['Septiembre', 30],
    ['Octubre', 31], ['Noviembre', 30], ['Diciembre', 31]
    ]

class InfoGraphic():
    """ Creates an infographic image """
    
    def __init__(self, image_filename):
        """ Constructor """
        self.filename = image_filename
        
    def generate_by_year(self, stations, daily_reports, year):
        """ Generates an infographic image showing temperature """

        def station_title(station):
            """ Returns the latitude and name of the station """ 
            hemisphere = 'N'
            if (station.latitude < 0):
                hemisphere = 'S'
            return "%s (%+1.0f%s, %i m)" % (station.name, station.latitude, hemisphere, station.altitude)

                    
        # Number of stations
        stations_num = stations.count()
        station_pos = dict()
        # Generate a dictionary with stations' row positions
        margin_x = 0
        margin_y = PIX_SIZE * 2
        pos_y = 0
        font = ImageFont.truetype(FONT, FONT_SIZE)
        for station in stations:
            font_size = font.getsize(station_title(station))
            if (font_size[0] > margin_x):
                margin_x = font_size[0]
            station_pos[station.name] = pos_y
            pos_y = pos_y + PIX_SIZE
        # Create image
        margin_x = margin_x + MARGIN_FONT
        size_x = margin_x + 368 * PIX_SIZE
        size_y = (stations_num + 3) * PIX_SIZE + margin_y
        im = Image.new("RGB", (size_x, size_y), "White")
        draw = ImageDraw.Draw(im)
        draw.setfont(font)
        # Draw title
        title = "Mapa de temperaturas %i - Datos AEMET - calima.linotipo.es" % (year)
        font_size = font.getsize(title)
        p_x = (size_x - font_size[0]) / 2
        p_y = 0
        draw.text((p_x, p_y), title, fill="Black")
        background_switch = True
        # Draw station names
        for station in stations:
            # Draw background
            color = (230,230,230) 
            if (background_switch == False):
           	    color = "White"
            background_switch = not background_switch
            p_y = margin_y + station_pos[station.name]
            p_x = 0
            draw.rectangle([p_x, p_y, margin_x - 1, p_y + PIX_SIZE - 1], fill=color)
            # Draw text
            font_size = font.getsize(station_title(station))
            p_x = margin_x - font_size[0] - int(MARGIN_FONT / 2)
            p_y = margin_y + station_pos[station.name] + int((PIX_SIZE - font_size[1]) / 2)
            draw.text((p_x, p_y), station_title(station), fill="Black")
        # Draw temperature palette
        i = 0
        for temperature in range(TEMP_MIN, TEMP_MAX + 1):
            p_x = margin_x + i * PIX_SIZE
            p_y = margin_y + (stations_num + 1) * PIX_SIZE
            color_index = 255 - int(float(temperature + abs(TEMP_MIN)) * COLOR_WEIGHT)
            color = scheme[color_index]
            # Draw rectangle
            draw.rectangle([p_x, p_y, p_x + PIX_SIZE - 1, p_y + PIX_SIZE - 1], fill=color)
            # Draw text
            font_size = font.getsize(str(temperature))
            p_x = p_x + int((PIX_SIZE - font_size[0]) / 2)
            draw.text((p_x, p_y), str(temperature), fill="White")
            i = i + 1
        # Draw temperatures
        for report in daily_reports:
            day_of_year = int(report.date.strftime('%j'))
            p_x = margin_x + (day_of_year - 1) * PIX_SIZE
            p_y = margin_y + station_pos[report.station.name]
            # Calculate color palette index
            color_index = 255 - int(float(report.avg_t + abs(TEMP_MIN)) * COLOR_WEIGHT)
            if color_index < 0:
                color_index = 0
            elif color_index > 255:
                color_index = 255
            color = scheme[color_index] 
            # Draw rectangle
            draw.rectangle([p_x, p_y, p_x + PIX_SIZE - 1, p_y + PIX_SIZE - 1], fill=color)
        # Draw months
        year_is_leap = calendar.isleap(year)
        days = 0
        for month in range(len(MONTHS)):
            # Month name
            (month_name, month_days) = MONTHS[month]
            font_size = font.getsize(month_name)
            p_x = margin_x + PIX_SIZE * days + int((PIX_SIZE * month_days - font_size[0]) / 2)
            p_y = PIX_SIZE
            draw.text((p_x, p_y), month_name, fill="Black")
            # Days
            days = days + MONTHS[month][1]
            # Leap year, add a day to the calendar
            if (month == 2 and year_is_leap):
            	days = days + 1
            # Draw month limit (finish)
            if (month < 11):
                p_x = margin_x + PIX_SIZE * days
                p_y = PIX_SIZE * 2
                draw.line((p_x, p_y, p_x, p_y + PIX_SIZE * stations_num), fill="Black")
        # Draw logo
        if (LOGO_IMAGE):
            logo = Image.open(LOGO_IMAGE)
            logo_size = 200
            logo.thumbnail((logo_size, logo_size), Image.NEAREST or Image.ANTIALIAS)
            p_x = size_x - logo.size[0]
            p_y = size_y - logo.size[1]
            im.paste(logo, (p_x, p_y, p_x + logo.size[0], p_y + logo.size[1]))
        del draw
        im.save(self.filename, "PNG")
        
    def image_by_year(self, year):
        """ Generate infographic by year """
        if (year < 1920 or year > 2050):
            return
        # Stations, ordered by latitude and longitude
        stations = Station.objects.all().order_by('-latitude', 'latitude')
        # Daily reports, ordered by date
        daily_reports = DailyReport.objects.filter(date__year=year).order_by('date').filter(avg_t__isnull=False)
        self.generate_by_year(stations, daily_reports, year)

class Command(BaseCommand):
    args = '<fichero.png> <año>'
    help = 'Genera un gráfico de información con el histórico de datos'

    def handle(self, *args, **options):
        image = args[0]
        year = int(args[1])
        graph = InfoGraphic(image)
        graph.image_by_year(year)
