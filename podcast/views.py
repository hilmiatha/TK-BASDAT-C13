from django.shortcuts import render
from django.db import connection
# from homepage.query import *
from utils import parse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# @csrf_exempt
def play_podcast(request):
    context = {
        'is_logged_in' : True,
        'user_type_info'  : {
            'is_pengguna_biasa' : True,
            'is_premium' : False,
            'is_label' : False,
            'is_podcaster' : False,
            'is_artist' : False,
            'is_songwriter' : False,
        },  
    }
    return render(request, 'play_podcast.html',context)

def manage_podcast(request):
    return render(request, 'manage_podcast.html')

def manage_episode(request):
    return render(request, 'manage_episode.html')