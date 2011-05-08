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

   def read(self, request, station_code=None):
        base = Station.objects
        
        if station_code:
            return base.get(code=station_code)
        else:
            return base.all()


class DailyReportHandler(BaseHandler):
   allowed_methods = ('GET',)
   model = DailyReport
   exclude = ('station',)

   def read(self, request, station_code=None):
        base = DailyReport.objects

        if station_code:
            return base.filter(station__code=station_code)
        else:
            return base.all()
