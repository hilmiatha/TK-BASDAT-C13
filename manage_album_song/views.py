from uuid import uuid4
from django.shortcuts import redirect, render
from django.db import connection
from manage_album_song.query import *
from utils import parse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def album(request):
    cursor = connection.cursor()
    if request.method == 'POST':
        uuid = str(uuid4())
        cursor.execute(create_album(), 
            [uuid, request.POST.get('judul'), str(request.POST.get('label'))])
    
    cursor.execute(get_all_labels())
    labels_obj = parse(cursor)
    cursor.execute(get_all_albums())
    albums_obj = parse(cursor)
    context = {
        'is_logged_in' : True,
        'user_type_info'  : {
            'is_pengguna_biasa' : False,
            'is_premium' : False,
            'is_label' : False,
            'is_podcaster' : False,
            'is_artist' : True,
            'is_songwriter' : False,
        },  
        'labels':labels_obj,
        'albums':albums_obj
    }
    return render(request, 'album.html',context)

def delete_album(request, id):
    cursor = connection.cursor()
    cursor.execute(delete_album_by_id(), [id])
    return redirect('album')

def songs(request):
    cursor = connection.cursor()
    if request.method == 'POST':
        print(request.POST)
        insert_song(request.POST.get('judul'), request.POST.get('durasi'), id_artist, id_album, songwriters)
    cursor.execute(get_all_artists())
    artists_obj = parse(cursor)
    cursor.execute(get_all_songwriters())
    songwriters_obj = parse(cursor)
    cursor.execute(get_all_genres())
    genres_obj = parse(cursor)
    print(cursor.execute(get_all_songs()))

    # print(genres_obj)
    context = {
        'is_logged_in' : True,
        'user_type_info'  : {
            'is_pengguna_biasa' : False,
            'is_premium' : False,
            'is_label' : False,
            'is_podcaster' : False,
            'is_artist' : True,
            'is_songwriter' : False,
        },  
        'artists':artists_obj,
        'songwriters':songwriters_obj,
        'genres':genres_obj,
    }
    return render(request, 'songs.html',context)