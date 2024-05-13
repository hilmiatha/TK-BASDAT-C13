from django.shortcuts import render
from django.db import connection
from royalti.query import *
from utils import parse

# Create your views here.
def check_royalti(request):
    return render(request, 'check_royalti.html')

def list_album(request):
    return render(request, 'list_album.html')

def list_song(request):
    return render(request, 'list_song.html')

def check_royalti(request):
    cursor = connection.cursor()
    artist = ''
    album = ''
    list_song = {}
    if request.session['is_artist']:
        cursor.execute(get_artist_by_email(), [request.session['email']])
        artist = parse(cursor)
        cursor.execute(get_song_konten_album_by_id_artist(), [artist[0].get('id')])
        data = parse(cursor)
        cursor.execute(get_song_by_id_artist(), [artist[0].get('id')])
        song = parse(cursor)
        cursor.execute(get_pemilik_hak_cipta_by_id(), [artist[0].get('id_pemilik_hak_cipta')])
        rate_royalti = parse(cursor)[0].get('rate_royalti')
        for obj in song:
            konten = None
            list_album = []
            cursor.execute(get_konten_by_id_konten(), [obj.get('id_konten')])
            konten = parse(cursor)
            cursor.execute(get_album_by_id_album(), [obj.get('id_album')])
            list_album.append(parse(cursor))
            jumlah_royalti = obj.get('total_play') * rate_royalti
            cursor.execute(create_royalti(), [artist[0].get('id_pemilik_hak_cipta'), obj.get('id_konten'), jumlah_royalti])
            cursor.execute(get_royalti_by_id(), [artist[0].get('id_pemilik_hak_cipta'), obj.get('id_konten')])
            royalti = parse(cursor)
            list_song[f"{obj.get('id_konten')}"] = {'konten':konten, 'album':list_album, 'song':obj, 'royalti':royalti[0]}

            # print(len(list_album), len(list_konten))
        # print(song)
        # print(list_konten)
        # print(list_album)
        # print(data)
        # print()
        print(list_song)
        print(len(list_song))
        pass
    elif request.session['is_songwriter']:
        pass
    elif request.session['is_label']:
        pass
    context = {
        'is_logged_in' : True,
        'user_type_info'  : {
            'is_pengguna_biasa' : False,
            'is_premium' : False,
            'is_label' : True,
            'is_podcaster' : False,
            'is_artist' : False,
            'is_songwriter' : False,
        },
        'artist':artist,
        'album':'',
        'song':list_song,
    }
    return render(request, 'check_royalti.html',context)

def list_album(request):
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
    }
    return render(request, 'list_album.html',context)

def list_song(request):
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
    }
    return render(request, 'list_song.html',context)