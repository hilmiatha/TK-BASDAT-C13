from django.db import connection
from django.shortcuts import render
from utils import parse
from .query import *

# Create your views here.
def hasil_pencarian(request):
    search_input = request.GET.get('query', '')
    cursor = connection.cursor()

    cursor.execute(search_query_song(search_input))
    song_result = parse(cursor)

    cursor.execute(search_query_podcast(search_input))
    podcast_result = parse(cursor)

    cursor.execute(search_query_user_playlist(search_input))
    user_playlist_result = parse(cursor)


    context = {
        'search_input' : search_input,
        'song_result' : song_result,
        'podcast_result' : podcast_result,
        'user_playlist_result' : user_playlist_result
    }
    
    return render(request, 'hasil_pencarian.html', context)