# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse

from caligo.models import Province, Station, DailyReport
from django.db.models import Avg, Max, Min, Count

# I know, this should be a manager or something
def max_temperature(queryset):
    a = queryset.aggregate(Max('max_t'))
    return queryset.filter(max_t=a['max_t__max'])

def min_temperature(queryset):
    a = queryset.aggregate(Min('min_t'))
    return queryset.filter(min_t=a['min_t__min'])

def max_squall(queryset):
    a = queryset.aggregate(Max('squall')) 
    return queryset.filter(squall=a['squall__max'])

def min_squall(queryset):
    a = queryset.aggregate(Min('squall')) 
    return queryset.filter(squall=a['squall__min'])

def max_precip(queryset):
    a = queryset.aggregate(Max('precip')) 
    return queryset.filter(precip=a['precip__max'])

def min_precip(queryset):
    a = queryset.aggregate(Min('precip')) 
    return queryset.filter(precip=a['precip__min']).exclude(precip=None)

def provinces(request, provinceId=None):
    # For specific province
    if provinceId:
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
        Province.objects.all().order_by('name')})

def stations(request, stationId=None, filtro=None):
    from datetime import datetime
    """ Parameters
        ?year
        ?month
        ?day
        stationId : the code of the station
        filtro: a special keyword for specific view (see urls.py)
    """
    if stationId:
        try:
            obj = Station.objects.get(code=stationId)
        except Station.DoesNotExist:
            return render_to_response('404.html', 
                {"text": "Station %s not found" % stationId})

        # Keyword for filter ....
        # Get the parameters form the GEt and generates the filter
        # keywords: year month day
        mapfilter = {
                'year': lambda w: ('date__year', w),
                'month': lambda w: ('date__month', w),
                'day': lambda w: ('date__day', w),
                'starts_year' : lambda w: ('date__gt', datetime(int(w)-1,12,31)),
                'ends_year' : lambda w: ('date__lt', datetime(int(w)+1,1,1)),
                }
        a = dict([ mapfilter[x](request.GET.get(x)) for x in request.GET if x
            in mapfilter])

        # Get the date order by date
        data = DailyReport.objects.filter(station=obj).order_by('date')

        # Apply the filters
        data_filtered = data.filter(**a)

        # I know, this should be in a manager, but I didn't have time
        if filtro == 'max_t':
            data_filtered = max_temperature(data_filtered)
        elif filtro == 'min_t':
            data_filtered = min_temperature(data_filtered)
        elif filtro == 'max_squall':
            data_filtered = max_squall(data_filtered)
        elif filtro == 'min_squall':
            data_filtered = min_squall(data_filtered)
        elif filtro == 'max_prec':
            data_filtered =  max_precip(data_filtered)
        elif filtro == 'min_prec':
            data_filtered = min_precip(data_filtered)

        return render_to_response('station.html', 
                {
                    'station' : obj,
                    'data'    : data_filtered,
                    'years'   : data.dates('date', 'year'),
                    'months'  : data.dates('date', 'month'),
                    'parameters' : request.GET,
                    })

    # General view
    return render_to_response('station_list.html', {'stations':
        Station.objects.all().order_by('name')})


def api(request):
    # API info page
    return render_to_response('api.html')

def about(request):
    # About info page
    return render_to_response('about.html')

def index_html(request):
    # index page
    return render_to_response('index.html')
