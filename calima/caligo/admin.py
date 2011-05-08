from django.contrib import admin
from caligo.models import Station, Province, DailyReport


admin.site.register(Province)
class DailyReportAdmin(admin.ModelAdmin):
    list_display = ('station', 'date')
    list_filter = ['date', 'station', ]

class StationAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'province')
    list_filter = ['province',]

admin.site.register(Station, StationAdmin)
admin.site.register(DailyReport, DailyReportAdmin)
