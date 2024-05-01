from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.db import connection
from .query import *
from utils import parse
from django.views.decorators.csrf import csrf_exempt
from .functions import *


##### =============================== FITUR 1 ============================================
def show_playlist(request):
    cursor = connection.cursor()
    cursor.execute(get_playlist('zaoqgo9@demo.net'))
    res = parse(cursor)
    context = {
        'playlists': res
    }
    return render(request, 'playlist_list.html',context)

def buat_playlist(request):
    if request.method == 'POST':
        # Get data from the form
        title = request.POST.get('judul')
        description = request.POST.get('deskripsi')

        # Placeholder: Process form data here (e.g., save to database)
        # For now, we'll just display a success message and redirect
        messages.success(request, f"Playlist '{title}' has been created successfully.")

        # Redirect to the playlist listing page (change 'show_playlist' to your actual URL name)
        return redirect('show_playlist')
    
    # If GET request or any other method, render an empty form
    return render(request, 'buat_playlist.html')

def playlist_detail(request, id_playlist): ######### INI FITUR 3 BERLAKU JUGA
    
    cursor = connection.cursor()
    cursor.execute(get_playlist_detail(id_playlist))
    res = parse(cursor)
    cursor.execute(get_playlist_info(id_playlist))
    res2 = parse(cursor)
    res2[0]['total_durasi'] = get_waktu_jam(res2[0].get('total_durasi'))
    context = {
        'playlist_song': res,
        'playlist_info': res2,
        'user_is_owner': True,
    }
    
    
    return render(request, 'playlist_detail.html', context)

def tambah_lagu_to_playlist(request, id_playlist):
    cursor = connection.cursor()
    cursor.execute(get_lagu())
    res = parse(cursor)
    context = {
        'lagu': res,
        'id_playlist': {'a':id_playlist},
    }
    return render(request, 'tambah_lagu_to_playlist.html', context)


def show_ubah_playlist(request, id_playlist):
    cursor = connection.cursor()
    cursor.execute(get_judul_deskripsi_playlist(id_playlist))
    res = parse(cursor)
    context = {
        'playlist': res[0]
    }
    print(res[0])
    return render(request, 'ubah_playlist.html', context)

##### =============================== FITUR 2 ============================================

def show_song_detailed(request,id_song='3b814ca4-20e2-4b82-ae7f-140bbf50536e'):
    cursor = connection.cursor()
    cursor.execute(get_atribut_lagu_except_songwriter(id_song))
    res = parse(cursor)
    cursor.execute(get_songwriter_from_song(id_song))
    res2 = parse(cursor)
    context = {
        'song_info': res[0],
        'songwriter': res2[0].get('songwriter').split(','),
        'genre' : res[0].get('genre').split(','),
        'user_is_premium' : True,
    }
    return render(request, '2_song_detailed.html', context)

def add_song_to_playlist(request, id_song='3b814ca4-20e2-4b82-ae7f-140bbf50536e'):
    USER_SEMENTARA = 'zaoqgo9@demo.net' ## implementasi front end dulu
    cursor = connection.cursor()
    cursor.execute(get_atribut_lagu_except_songwriter(id_song))
    res = parse(cursor)
    cursor.execute(get_playlist_per_user(USER_SEMENTARA))
    res2 = parse(cursor)
    context = {
        'song_info': res[0],
        'playlist_info': res2,
    }
    
    print(context)
    return render(request, '2_add_song_to_playlist.html', context)
    