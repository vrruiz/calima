# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse

from caligo.models import Province
def provinces(request, provinceId=None):
    if provinceId:
        obj = Province.objects.get(id=provinceId)
        # Return stuff
        return render_to_response('province.html', {'province': obj})
    return render_to_response('province_list.html', {'provinces':
        Province.objects.all()})

