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
    values['yoffset'] = data[0].value

    if(len(dataset)>max_points):
        spacing = int(math.floor(len(dataset)/max_points))
    else:
        spacing = 1

    point_counter = 0
    for point in data:
        point_counter += 1

        if(point_counter%spacing==0):
            dataset.append({
                # 'time':int(time.mktime(point.time.timetuple()))-int(time.mktime(data[0].time.timetuple())),
                'time': time.mktime(point.time.timetuple()),
                'value':point.value-values['yoffset'],
                })

    values['data'] = dataset
    values['coincount'] = data.order_by('-time')[0].value


    # values['mine_rate']['10s'] = (dataset[:-1]['value']-dataset[:-2]['value'])/10
    # values['mine_rate']['1m'] = (dataset[:-1]['value']-dataset[:-7]['value'])/60
    # values['mine_rate']['5m'] = (dataset[:-1]['value']-dataset[:-31]['value'])/300
    # values['mine_rate']['15m'] = (dataset[:-1]['value']-dataset[:-91]['value'])/900


    return render(request, "graph.html", values)
