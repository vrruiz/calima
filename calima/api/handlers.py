from piston.handler import BaseHandler
from caligo.models import Station, DailyReport


class StationHandler(BaseHandler):
   allowed_methods = ('GET',)
   model = Station  

   def read(self, request, code=None):
        base = Station.objects
        
        if code:
            return base.get(code=code)
        else:
            return base.all()