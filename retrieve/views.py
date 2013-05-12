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

    if(DataPoint.objects.count() > max_points):
        spacing = int(math.ceil(float(DataPoint.objects.count()) / max_points))
        print "Spacing: "+str(spacing)
        if spacing < 1:
            spacing = 1
    else:
        spacing = 1

    point_counter = 0
    for point in data:
        point_counter += 1

        if(point_counter % spacing == 0):
            dataset.append({
                'time': time.mktime(point.time.timetuple()),
                'value': point.value,
            })

    values['data'] = dataset

    mostRecentFirst = data.order_by('-time')

    values['coin_count'] = mostRecentFirst[0].value
    values['difficulty'] = mostRecentFirst[0].difficulty

    coins_until_next_increase = (values['difficulty']-7)*205000 - values['coin_count']

    print coins_until_next_increase

    values['mine_rate'] = dict()

    if(len(mostRecentFirst) > 1):
        values['mine_rate']['10s'] = float((mostRecentFirst[
                                           0].value - mostRecentFirst[1].value)) / 10
    if(len(mostRecentFirst) > 6):
        values['mine_rate']['1m'] = float((mostRecentFirst[
                                          0].value - mostRecentFirst[6].value)) / 60
    if(len(mostRecentFirst) > 30):
        values['mine_rate']['5m'] = float((mostRecentFirst[
                                          0].value - mostRecentFirst[30].value)) / 300
    if(len(mostRecentFirst) > 90):
        values['mine_rate']['15m'] = float((mostRecentFirst[
                                           0].value - mostRecentFirst[90].value)) / 900

        #Logic for ETA goes here:




    return render(request, "graph.html", values)
