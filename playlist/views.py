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
    cursor.execute(get_playlist(request.session['email']))
    res = parse(cursor)
    context = {
        'playlists': res,
    }
    return render(request, 'playlist_list.html',context)

def buat_playlist(request):
    if request.method == 'POST':
        # Get data from the form
        title = request.POST.get('judul')
        description = request.POST.get('deskripsi')
        
        cursor = connection.cursor()
        cursor.execute(insert_playlist(request.session['email'], title, description))
        connection.commit()
        
        return redirect('show_playlist')
    
    return render(request, 'buat_playlist.html')

def playlist_detail(request, id_playlist): ######### INI FITUR 3 BERLAKU JUGA
    
    cursor = connection.cursor()
    cursor.execute(f"SELECT nama FROM akun a, user_playlist up WHERE a.email = up.email_pembuat AND up.id_playlist = '{id_playlist}';")
    nama_pembuat = parse(cursor)[0].get('nama')
    cursor.execute(get_playlist_detail(id_playlist))
    res = parse(cursor)
    cursor.execute(get_playlist_info(id_playlist))
    res2 = parse(cursor)
    res2[0]['total_durasi'] = get_waktu_jam(res2[0].get('total_durasi'))
    context = {
        'playlist_song': res,
        'playlist_info': res2,
        'id_playlist_root' : id_playlist,
        'nama_pembuat' : nama_pembuat, 
        
    }
    
    
    return render(request, 'playlist_detail.html', context)

def tambah_lagu_to_playlist(request, id_playlist):
    cursor = connection.cursor()
    cursor.execute(get_lagu())
    res = parse(cursor)
    context = {
        'lagu': res,
    }
    
    if request.method == 'POST':
        # Get data from the form
        id_lagu = request.POST.get('lagu')
        
        cursor.execute(f"SELECT * FROM playlist_song WHERE id_playlist = '{id_playlist}' AND id_song = '{id_lagu}';")
        if len(parse(cursor)) > 0:
            # Lagu sudah ada di playlist
            context['error_message'] = 'Lagu sudah ada di playlist'
            return render(request, 'tambah_lagu_to_playlist.html', context)
        
        cursor.execute(f"SELECT durasi FROM konten WHERE id = '{id_lagu}';")
        durasi =parse(cursor)[0].get('durasi')
        
        cursor.execute(insert_playlist_song(id_playlist, id_lagu, durasi))
        connection.commit()
        
        return redirect('playlist_detail', id_playlist=id_playlist)
    
    return render(request, 'tambah_lagu_to_playlist.html', context)


def show_ubah_playlist(request, id_playlist):
    cursor = connection.cursor()
    cursor.execute(get_judul_deskripsi_playlist(id_playlist))
    res = parse(cursor)
    context = {
        'playlist': res[0]
    }
    if request.method == 'POST':
        # Get data from the form
        title = request.POST.get('judul')
        description = request.POST.get('deskripsi')
        
        cursor.execute(f"SELECT id_user_playlist FROM user_playlist WHERE id_playlist = '{id_playlist}';")
        id_user_playlist = parse(cursor)[0].get('id_user_playlist')
        
        cursor.execute(update_playlist(title, description, id_user_playlist))
        connection.commit()
        
        return redirect('show_playlist')
    return render(request, 'ubah_playlist.html', context)


def hapus_playlist(request, id_playlist):
    cursor = connection.cursor()
    cursor.execute(f"SELECT id_user_playlist FROM user_playlist WHERE id_playlist = '{id_playlist}';")
    id_user_playlist = parse(cursor)[0].get('id_user_playlist')
    cursor.execute(delete_playlist(id_user_playlist, id_playlist))
    connection.commit()
    return redirect('show_playlist')


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
        'is_logged_in' : True,
        'user_type_info'  : {
            'is_pengguna_biasa' : True,
            'is_premium' : True,
            'is_label' : False,
            'is_podcaster' : False,
            'is_artist' : False,
            'is_songwriter' : False,
        },
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
    
    print(context)
    return render(request, '2_add_song_to_playlist.html', context)
    
