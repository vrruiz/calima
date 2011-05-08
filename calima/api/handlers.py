from piston.handler import BaseHandler
from caligo.models import Province, Station, DailyReport


class ProvinceHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Province

    def read(self, request, name=None):
        base = Province.objects
        
        if name:
            return base.get(name=name)
        else:
            return base.all()


class StationHandler(BaseHandler):
   allowed_methods = ('GET',)
   model = Station  

   def read(self, request, code=None):
        base = Station.objects
        
        if code:
            return base.get(code=code)
        else:
            return base.all()