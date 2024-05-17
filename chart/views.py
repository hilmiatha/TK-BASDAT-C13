from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.db import connection
from .query import *
from utils import parse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def see_chart(request):
    cursor = connection.cursor()
    cursor.execute(get_charts())
    res = parse(cursor)
    context = {
        'charts' : res,
    }
    return render(request, 'see_chart.html',context)

@csrf_exempt
def see_songs_chart(request, id_playlist):
    cursor = connection.cursor()
    cursor.execute(get_songs_chart(id_playlist))
    res = parse(cursor)
    cursor.execute(get_chart_info(id_playlist))
    res2 = parse(cursor)
    context = {
        'chart' : res2,
        'chart_songs' : res,
    }
    return render(request, 'see_songs_chart.html',context)