from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.db import connection
from .query import *
from utils import parse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
# def see_chart(request):
#     return render(request, 'see_chart.html')


# def see_songs_chart(request):
#     return render(request, 'see_songs_chart.html')

def see_chart(request):
    cursor = connection.cursor()
    cursor.execute(get_charts())
    res = parse(cursor)
    context = {
        'charts' : res,
        'is_logged_in' : True,
        'user_type_info'  : {
            'is_pengguna_biasa' : True,
            'is_premium' : True,
            'is_label' : False,
            'is_podcaster' : False,
            'is_artist' : True,
            'is_songwriter' : False,
        },  
    }
    return render(request, 'see_chart.html',context)

def see_songs_chart(request, id_playlist):
    cursor = connection.cursor()
    cursor.execute(get_songs_chart(id_playlist))
    res = parse(cursor)
    cursor.execute(get_chart_info(id_playlist))
    res2 = parse(cursor)
    context = {
        'chart' : res2,
        'chart_songs' : res,
        'is_logged_in' : True,
        'user_type_info'  : {
            'is_pengguna_biasa' : True,
            'is_premium' : True,
            'is_label' : False,
            'is_podcaster' : False,
            'is_artist' : True,
            'is_songwriter' : False,
        },  
    }
    return render(request, 'see_songs_chart.html',context)