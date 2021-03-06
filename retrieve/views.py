# Create your views here.
from django.shortcuts import render
from retrieve.models import DataPoint
import time
import math
import datetime


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

    coins_until_next_increase = (values['difficulty']-6)*205000 - values['coin_count']

    values['mine_rate'] = dict()


    #TODO: Refactor this into a method for n second averages
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
    
    if(len(mostRecentFirst) > 360):
        values['mine_rate']['1hr'] = float((mostRecentFirst[
                                           0].value - mostRecentFirst[360].value)) / 3600

        #Logic for ETA goes here:
        seconds_until_increase = float(coins_until_next_increase)/values['mine_rate']['1hr']
        values['increase_date'] = datetime.datetime.fromtimestamp(time.time()+seconds_until_increase)



    previous_difficulty_threshold = (values['difficulty']-7)*205000

    current_difficulty_data = DataPoint.objects.filter(value__gt=previous_difficulty_threshold)


    #Spacing for current graph
    if(current_difficulty_data.count() > max_points):
        spacing = int(math.ceil(float(current_difficulty_data.count()) / max_points))
        if spacing < 1:
            spacing = 1
    else:
        spacing = 1


    #Space data evenly
    values['difficulty_dataset'] = []
    point_counter = 0
    for point in current_difficulty_data:
        point_counter += 1

        if(point_counter % spacing == 0):
            values['difficulty_dataset'].append({
                'time': time.mktime(point.time.timetuple()),
                'value': point.value,
            })


    return render(request, "graph.html", values)
