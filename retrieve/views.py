# Create your views here.
from django.shortcuts import render
from retrieve.models import DataPoint
import time


def graph(request):
    values = dict()

    data = DataPoint.objects.all()
    dataset = []

    for point in data:
        int(time.mktime(point.time.timetuple())*1000)
        dataset.append({'time':int(time.mktime(point.time.timetuple())*1000)-int(time.mktime(data[0].time.timetuple())*1000), 'value':point.value-data[0].value})

    values['data'] = dataset


    return render(request, "graph.html", values)
