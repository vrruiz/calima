# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse

from caligo.models import Province, Station, DailyReport


def provinces(request, provinceId=None):
    # For specific province
    if provinceId:
        # TODO Error Id
        try:
            obj = Province.objects.get(id=provinceId)
        except Province.DoesNotExist:
            return render_to_response('404.html',
                    {"text": "Province %s not found" % provinceId})
        return render_to_response('province.html', 
                {
                    'province': obj,
                    'stations': obj.stations.all(),
                    })

    # General view
    return render_to_response('province_list.html', {'provinces':
        Province.objects.all()})

def stations(request, stationId=None, filtro=None):
    from datetime import datetime
    """ Parameters
        ?year
        ? month
    """
    if stationId:
        print filtro
        try:
            obj = Station.objects.get(code=stationId)
        except Station.DoesNotExist:
            return render_to_response('404.html', 
                {"text": "Station %s not found" % stationId})

        # Keyword for filter ....
        # Get the parameters form the GEt and generates the filter
        mapfilter = {'year': 'date__year',
                     'month': 'date__month'}
        a = dict([ (mapfilter[x] , request.GET.get(x)) for x in request.GET if x
            in mapfilter])

        # Get the date order by date
        data = DailyReport.objects.filter(station=obj).order_by('date')

        # Apply the filters
        data_filtered = data.filter(**a)

        if filtro:
            data_filtered = data_filtered.values_list('date', filtro)
        # Data for the char, has to be converted
        # Defina the data

        return render_to_response('station.html', 
                {
                    'station' : obj,
                    'data'    : data_filtered,
                    'years'   : data.dates('date', 'year'),
                    'months'  : data.dates('date', 'month'),
                    'parameters' : request.GET.urlencode(),
                    'filtered' : filtro != None,
                    })

    # General view
    return render_to_response('station_list.html', {'stations':
        Station.objects.all()})


def api(request):
    # API info page
    return render_to_response('api.html')

def about(request):
    # About info page
    return render_to_response('about.html')

def index_html(request):
    # index page
    return render_to_response('index.html')
