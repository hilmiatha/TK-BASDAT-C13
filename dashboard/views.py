from uuid import uuid4
from django.shortcuts import redirect, render
from django.db import connection
from homepage.query import *
from dashboard.query import *
from utils import parse
# Create your views here.
def dashboard(request):
    email = request.session['email']
    cursor = connection.cursor()
    user = None
    status_langganan = 'Non Premium'
    role = []
    role_str = ''
    label = None
    playlist = None
    daftar_lagu = []
    daftar_podcast = []
    daftar_album = []
    
    if request.session['is_pengguna_biasa']:
        cursor.execute(get_user_by_email(), [email])
        user = parse(cursor)
        cursor.execute(get_user_playlist(), [email])
        playlist = parse(cursor)
        if request.session['is_premium']:
            status_langganan='Premium'
        
        if request.session['is_artist']:
            role.append('Artist')
            cursor.execute(get_song_by_id_artist(), [email])
            daftar_lagu.extend(parse(cursor))
        if request.session['is_podcaster']:
            role.append('Podcaster') 
            cursor.execute(get_podcast_by_podcaster(), [email])
            daftar_podcast.extend(parse(cursor))
        if request.session['is_songwriter']:
            role.append('Songwriter')
            cursor.execute(get_song_by_songwriter(), [email])
            daftar_lagu.extend(parse(cursor))
        role_str = ", ".join(role)
    elif request.session['is_label']:
        cursor.execute(get_label_by_email(), [email])
        label = parse(cursor)
        cursor.execute(get_album_by_id_label(), [label[0].get('id')])
        daftar_album.extend(parse(cursor))
    seen = set()
    unique_daftar_lagu = []
    for item in daftar_lagu:
        # Consider the item 'id' or another unique identifier for hashing
        identifier = item.get('id_konten')  # Assuming 'id' is a unique field in the dictionary
        if identifier not in seen:
            seen.add(identifier)
            unique_daftar_lagu.append(item)
    daftar_lagu = unique_daftar_lagu
    context = {
        'is_logged_in' : True,
        'user_type_info'  : {
            'is_pengguna_biasa' : True,
            'is_premium' : True,
            'is_label' : False,
            'is_podcaster' : False,
            'is_artist' : False,
            'is_songwriter' : False,
        },  
        'user':user,
        'label':label,
        'status_langganan':status_langganan,
        'role':role_str,
        'playlist':playlist,
        'daftar_lagu':daftar_lagu,
        'daftar_podcast':daftar_podcast,
        'daftar_album':daftar_album
    }
    return render(request, 'dashboard.html',context)