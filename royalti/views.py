from django.shortcuts import render
from django.db import connection
from royalti.query import *
from utils import parse

# Create your views here.
def check_royalti(request):
    cursor = connection.cursor()
    artist = ''
    album = ''
    user = None
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
        user = artist
        print(list_song)
        print(len(list_song))
    elif request.session['is_songwriter']:
        cursor.execute(get_songwriter_by_email(), [request.session['email']])
        songwriter = parse(cursor)
        cursor.execute(get_pemilik_hak_cipta_by_id(), [songwriter[0].get('id_pemilik_hak_cipta')])
        rate_royalti = parse(cursor)[0].get('rate_royalti')
        cursor.execute(get_id_song_by_songwriter(), [songwriter[0].get('id')])
        list_id_song = parse(cursor)
        for id_song in list_id_song:
            cursor.execute(get_song_by_id_konten(), [id_song.get('id_song')])
            song = parse(cursor)[0]
            konten = None
            list_album = []
            cursor.execute(get_konten_by_id_konten(), [id_song.get('id_song')])
            konten = parse(cursor)
            cursor.execute(get_album_by_id_album(), [id_song.get('id_song')])
            list_album.append(parse(cursor))
            jumlah_royalti = song.get('total_play') * rate_royalti
            cursor.execute(create_royalti(), [songwriter[0].get('id_pemilik_hak_cipta'), id_song.get('id_song'), jumlah_royalti])
            cursor.execute(get_royalti_by_id(), [songwriter[0].get('id_pemilik_hak_cipta'), id_song.get('id_song')])
            royalti = parse(cursor)
            list_song[f"{song.get('id_konten')}"] = {'konten':konten, 'album':list_album, 'song':song, 'royalti':royalti[0]}
        user=songwriter
    elif request.session['is_label']:
        cursor.execute(get_label_by_email(), [request.session['email']])
        label = parse(cursor)
        for obj in label:
            cursor.execute(get_pemilik_hak_cipta_by_id(), [obj.get('id_pemilik_hak_cipta')])
            rate_royalti = parse(cursor)[0].get('rate_royalti')
            cursor.execute(get_album_by_id_label(), [obj.get('id')])
            albums = parse(cursor)
            for album in albums:
                cursor.execute(get_song_by_id_album(), [album.get('id')])
                songs = parse(cursor)
                for song in songs:
                    print(song)
                    konten = None
                    list_album = []
                    cursor.execute(get_konten_by_id_konten(), [song.get('id_konten')])
                    konten = parse(cursor)
                    # cursor.execute(get_album_by_id_album(), [song.get('id_album')])
                    list_album.append([album])
                    jumlah_royalti = song.get('total_play') * rate_royalti
                    cursor.execute(create_royalti(), [obj.get('id_pemilik_hak_cipta'), song.get('id_konten'), jumlah_royalti])
                    cursor.execute(get_royalti_by_id(), [obj.get('id_pemilik_hak_cipta'), song.get('id_konten')])
                    royalti = parse(cursor)
                    list_song[f"{song.get('id_konten')}"] = {'konten':konten, 'album':list_album, 'song':song, 'royalti':royalti[0]}
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
        'user':user,
        'album':'',
        'song':list_song,
    }
    return render(request, 'check_royalti.html',context)

def list_album(request):
    cursor = connection.cursor()
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

def list_song(request, id):
    cursor = connection.cursor()
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