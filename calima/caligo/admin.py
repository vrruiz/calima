from django.contrib import admin
from caligo.models import Station, Province, DailyReport


admin.site.register(Station)
admin.site.register(Province)
admin.site.register(DailyReport)
