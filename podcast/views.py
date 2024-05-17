from pyexpat.errors import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db import DatabaseError, connection, transaction
from django.urls import reverse
from pyexpat.errors import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db import DatabaseError, connection, transaction
from django.urls import reverse
from .query import *
from utils import parse
from django.views.decorators.csrf import csrf_exempt
from .functions import *

# Create your views here.


@csrf_exempt
def play_podcast(request, id_podcast):
    cursor = connection.cursor()
    cursor.execute(get_podcast(id_podcast))
    res = parse(cursor)
    cursor.execute(get_episodes(id_podcast))
    res2 = parse(cursor)
    res[0]['durasi'] = get_waktu_jam(res[0].get('durasi'))
    for i in range(len(res2)):
        res2[i]['durasi'] = get_waktu_jam(res2[i].get('durasi'))
    context = {
        'info_podcast' : res[0],
        'genre' : res[0].get('genre').split(','),
        'episodes' : res2,
    }
    return render(request, 'play_podcast.html',context)

def manage_podcast(request):
    email = request.session['email']
    cursor = connection.cursor()
    cursor.execute(get_genres())
    res = parse(cursor)
    cursor.execute(get_podcasts_list(email))
    res2 = parse(cursor)
    for i in range(len(res2)):
        res2[i]['durasi'] = get_waktu_jam(res2[i].get('durasi'))
    context = {
        'genres' : res,
        'podcasts' : res2
    }
    return render(request, 'manage_podcast.html', context)

def manage_episode(request):
    return render(request, 'manage_episode.html')


# def manage_podcast(request):
#     context = {
#         'is_logged_in' : True,
#         'user_type_info'  : {
#             'is_pengguna_biasa' : False,
#             'is_premium' : False,
#             'is_label' : False,
#             'is_podcaster' : True,
#             'is_artist' : False,
#             'is_songwriter' : False,
#         },  
#     }
#     return render(request, 'manage_podcast.html',context)

# def manage_episode(request):
#     context = {
#         'is_logged_in' : True,
#         'user_type_info'  : {
#             'is_pengguna_biasa' : False,
#             'is_premium' : False,
#             'is_label' : False,
#             'is_podcaster' : True,
#             'is_artist' : False,
#             'is_songwriter' : False,
#         },  
#     }
#     return render(request, 'manage_episode.html',context)