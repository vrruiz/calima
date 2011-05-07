from django.contrib import admin
from caligo.models import Station, Province, DailyReport


admin.site.register(Station)
admin.site.register(Province)
class DailyReportAdmin(admin.ModelAdmin):
    list_display = ('station', 'date')

    list_filter = ['date']

admin.site.register(DailyReport, DailyReportAdmin)
