# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse

from caligo.models import Province, Station

def provinces(request, provinceId=None):
    # For specific province
    if provinceId:
        # TODO Error Id
        try:
            obj = Province.objects.get(id=provinceId)
        except Province.DoesNotExist:
            return render_to_response('404.html',
                    {"text": "Province %s not found" % provinceId})
        return render_to_response('province.html', {'province': obj})

    # General view
    return render_to_response('province_list.html', {'provinces':
        Province.objects.all()})

def stations(request, stationId=None):
    if stationId:
        try:
            obj = Station.objects.get(code=stationId)
        except Station.DoesNotExist:
            return render_to_response('404.html', 
                {"text": "Station %s not found" % stationId})
        return render_to_response('station.html', {'station': obj})

    # General view
    return render_to_response('station_list.html', {'stations':
        Station.objects.all()})


