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
        print(request.POST)
        uuid = str(uuid4())
        cursor.execute(create_album(), 
            [uuid, request.POST.get('judul'), str(request.POST.get('label'))])
        insert_song(request.POST.get('judul_lagu'), request.POST.get('duration'), request.POST.get('id_artist'), uuid, request.POST.getlist('songwriter'), request.POST.getlist('genre'))
    
    if request.session['is_label']:
        cursor.execute(get_label_by_email(), [request.session['email']])
        label = parse(cursor)[0]
        cursor.execute(get_album_by_id_label(), [label.get('id')])
        albums = parse(cursor)
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
            'albums':albums
        }
        return render(request, 'list_album.html',context)
    
    if request.session['is_artist']:
        cursor.execute(get_album_by_artist(), [request.session['email']])
        albums_obj = parse(cursor)
        cursor.execute(get_artist_by_email(), [request.session['email']])
    if request.session['is_songwriter']:
        cursor.execute(get_album_by_songwriter(), [request.session['email']])
        albums_obj = parse(cursor)
        cursor.execute(get_songwriter_by_email(), [request.session['email']])
    user = parse(cursor)
    cursor.execute(get_all_labels())
    labels_obj = parse(cursor)
    cursor.execute(get_all_artists())
    artists_obj = parse(cursor)
    cursor.execute(get_all_songwriters())
    songwriters_obj = parse(cursor)
    cursor.execute(get_all_genres())
    genres_obj = parse(cursor)
    cursor.execute(get_all_akuns())
    print(parse(cursor))

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
        'albums':albums_obj,
        'artists':artists_obj,
        'songwriters':songwriters_obj,
        'genres':genres_obj,
        'user':user,
    }
    return render(request, 'album.html',context)

def delete_album(request, id):
    cursor = connection.cursor()
    cursor.execute(delete_album_by_id(), [id])
    return redirect('album')

def delete_song(request, id):
    cursor = connection.cursor()
    cursor.execute(delete_song_by_id(), [id])
    return redirect('songs',id=request.GET.get('album_id'))

def songs(request, id):
    cursor = connection.cursor()
    if request.method == 'POST':
        print(request.POST)
        insert_song(request.POST.get('judul'), request.POST.get('duration'), request.POST.get('id_artist'), id, request.POST.getlist('songwriter'), request.POST.getlist('genre'))
    
    if request.session['is_label']:
        cursor.execute(get_song_konten_by_id_album(), [id])
        songs = parse(cursor)
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
            'songs':songs
        }
    return render(request, 'list_song.html',context)
    if request.session['is_artist']:
        cursor.execute(get_album_by_artist(), [request.session['email']])
        albums_obj = parse(cursor)
        cursor.execute(get_artist_by_email(), [request.session['email']])
    if request.session['is_songwriter']:
        cursor.execute(get_album_by_songwriter(), [request.session['email']])
        albums_obj = parse(cursor)
        cursor.execute(get_songwriter_by_email(), [request.session['email']])
    user = parse(cursor)
    cursor.execute(get_album_by_id(), [id])
    album = parse(cursor)[0]
    cursor.execute(get_all_artists())
    artists_obj = parse(cursor)
    cursor.execute(get_all_songwriters())
    songwriters_obj = parse(cursor)
    cursor.execute(get_all_genres())
    genres_obj = parse(cursor)
    cursor.execute(get_song_konten_by_id_album(), [id])
    songs = parse(cursor)

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
        'user':user,
        'album_id':album.get('id'),
        'album':album,
        'artists':artists_obj,
        'songwriters':songwriters_obj,
        'genres':genres_obj,
        'songs':songs,
    }
    return render(request, 'songs.html',context)