from retrieve.models import DataPoint
import urllib2
import json
from django.core.management.base import NoArgsCommand
import time


class Command(NoArgsCommand):

    def handle(self, *args, **options):
        while True:
            try:
                f = urllib2.urlopen('http://server.bloocoin.org/')
                output = json.loads(f.read())

                datapoint = DataPoint()

                datapoint.value = output['coins']
                datapoint.difficulty = output['difficulty']

                datapoint.save()
                print "Data point logged."
            except:
                print "Error."
            time.sleep(10)