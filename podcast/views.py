from django.shortcuts import render
from django.db import connection
# from homepage.query import *
from utils import parse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# @csrf_exempt
def test_view(request):
    return render(request, 'play_podcast.html')

def manage_podcast(request):
    return render(request, 'manage_podcast.html')

def manage_episode(request):
    return render(request, 'manage_episode.html')