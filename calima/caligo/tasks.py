import os
from datetime import timedelta

from celery.decorators import task, periodic_task
from django.conf import settings

from caligo.models import station_importer

# Execute every 24 hours
@periodic_task(run_every=timedelta(hours=24))
def updateStation():
    """ 
        Periodic task that updates the lastest anual data and
        import it to the model
    """

    try:
        path = settings.BASEDIR_DATA
    except AttributeError:
        # This should not happen I guess
        path = '/tmp/'
    calima = Calima(path=path)
    calima.actualizar()
    station_importer(calima.estaciones)

