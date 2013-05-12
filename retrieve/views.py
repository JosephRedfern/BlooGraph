# Create your views here.
from django.shortcuts import render
from retrieve.models import DataPoint
import time
import math


def graph(request):
    values = dict()

    data = DataPoint.objects.all()
    dataset = []

    max_points = 1000
    if(len(dataset)>max_points):
        spacing = int(math.floor(len(dataset)/max_points))
    else:
        spacing = 1

    point_counter = 0
    for point in data:
        point_counter += 1

        if(point_counter%spacing==0):
            dataset.append({
                'time':int(time.mktime(point.time.timetuple()))-int(time.mktime(data[0].time.timetuple())),
                'value':point.value-data[0].value,
                })

    values['data'] = dataset


    return render(request, "graph.html", values)
