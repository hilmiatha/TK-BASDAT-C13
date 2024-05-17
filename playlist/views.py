from pyexpat.errors import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db import DatabaseError, connection, transaction
from django.urls import reverse
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

        try:
            with transaction.atomic():
                cursor.execute(f"SELECT durasi FROM konten WHERE id = '{id_lagu}';")
                durasi = parse(cursor)[0].get('durasi')

                cursor.execute(insert_playlist_song(id_playlist, id_lagu, durasi))
            
            return redirect('playlist_detail', id_playlist=id_playlist)

        except DatabaseError as e:
            if 'Lagu sudah ada dalam playlist' in str(e):
                context['error_message'] = 'Lagu sudah ada dalam playlist'
            else:
                print(str(e))
                context['error_message'] = 'Terjadi kesalahan saat menambahkan lagu ke playlist. Silakan coba lagi.'
            return render(request, 'tambah_lagu_to_playlist.html', context)
    
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


def hapus_lagu_dari_playlist(request, id_playlist, id_lagu):
    cursor = connection.cursor()
    cursor.execute(delete_song_from_playlist(id_playlist, id_lagu))
    connection.commit()
    return redirect('playlist_detail', id_playlist=id_playlist)


##### =============================== FITUR 2 ============================================

def show_song_detailed(request,id_song):
    cursor = connection.cursor()
    cursor.execute(get_atribut_lagu_except_songwriter(id_song))
    res = parse(cursor)
    cursor.execute(get_songwriter_from_song(id_song))
    res2 = parse(cursor)
    context = {
        'song_info': res[0],
        'songwriter': res2[0].get('songwriter').split(','),
        'genre' : res[0].get('genre').split(','),
    }
    # play song post request
    if request.method == 'POST':
        value_play = request.POST.get('progress')
        if int(value_play) >= 70:
            cursor.execute(f"INSERT INTO akun_play_song (email_pemain, id_song, waktu) VALUES ('{request.session['email']}', '{id_song}', current_timestamp);UPDATE song SET total_play = total_play + 1 WHERE id_konten = '{id_song}';")
            connection.commit()
            cursor.execute(get_atribut_lagu_except_songwriter(id_song))
            res = parse(cursor)
            context['song_info'] = res[0]
            return render(request, '2_song_detailed.html', context)

    return render(request, '2_song_detailed.html', context)

def add_song_to_playlist(request, id_song):
    email = request.session['email']
    cursor = connection.cursor()
    cursor.execute(get_atribut_lagu_except_songwriter(id_song))
    res = parse(cursor)
    cursor.execute(get_playlist_per_user(email))
    res2 = parse(cursor)
    context = {
        'song_info': res[0],
        'playlist_info': res2,
    }

    if request.method == 'POST':
        id_playlist = request.POST.get('playlist')

        try:
            with transaction.atomic():
                cursor.execute(f"SELECT durasi FROM konten WHERE id = '{id_song}';")
                durasi = parse(cursor)[0].get('durasi')

                cursor.execute(insert_playlist_song(id_playlist, id_song, durasi))
            
            context.update({
                'result_message': f'Berhasil menambahkan lagu "{res[0]["judul_lagu"]}" ke playlist.',
                'success': True,
                'playlist_url': reverse('playlist_detail', args=[id_playlist]),
            })
            return render(request, 'result.html', context)

        except DatabaseError as e:
            if 'Lagu sudah ada dalam playlist' in str(e):
                context.update({
                    'result_message': 'Lagu sudah ada di playlist',
                    'success': False,
                })
            else:
                context.update({
                    'result_message': 'Terjadi kesalahan saat menambahkan lagu ke playlist. Silakan coba lagi.',
                    'success': False,
                })
            return render(request, 'result.html', context)
    
    return render(request, '2_add_song_to_playlist.html', context)




def download_song(request, id_song):
    cursor = connection.cursor()
    context = {'id_song': id_song,}
    
    try:
        with transaction.atomic():
            cursor.execute(f"INSERT INTO downloaded_song (id_song, email_downloader) VALUES ('{id_song}', '{request.session['email']}');")
            cursor.execute(f"UPDATE song SET total_download = total_download + 1 WHERE id_konten = '{id_song}';")

        context.update({
            'result_message': f'Berhasil mengunduh Lagu dengan judul "{get_song_title(id_song)}"!',
            'download_success': True,
            # 'download_list_url': reverse('#'), ##BELOM NUNGGU FITUR DOWNLOADED LIST
        })
    except DatabaseError as e:
        if 'Lagu sudah pernah diunduh' in str(e):
            context.update({
                'result_message': f'Lagu dengan judul "{get_song_title(id_song)}" sudah pernah diunduh!',
                'download_success': False,
            })
        else:
            print(str(e))
            context.update({
                'result_message': 'Terjadi kesalahan saat mengunduh lagu. Silakan coba lagi.',
                'download_success': False,
            })

    return render(request, 'download_result.html', context)

def get_song_title(id_song):
    cursor = connection.cursor()
    cursor.execute(f"SELECT judul FROM konten WHERE id = %s", [id_song])
    result = parse(cursor)
    if result:
        return result[0]['judul']
    return "Unknown Song"






# ================================== FITUR 3 ========================================

def shuffle_play(request, id_playlist):
    cursor = connection.cursor()
    cursor.execute(f"SELECT email_pembuat  FROM user_playlist WHERE id_playlist = '{id_playlist}';")
    email_pembuat = parse(cursor)[0].get('email_pembuat')
    cursor.execute(f"SELECT id_user_playlist FROM user_playlist WHERE id_playlist = '{id_playlist}';")
    id_user_playlist = parse(cursor)[0].get('id_user_playlist')
    cursor.execute(f"INSERT INTO akun_play_user_playlist (email_pemain, id_user_playlist, email_pembuat, waktu) VALUES ('{request.session['email']}', '{id_user_playlist}', '{email_pembuat}', current_timestamp);")
    return redirect('playlist_detail', id_playlist=id_playlist)

def play_song(request,id_playlist,id_song):
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO akun_play_song (email_pemain, id_song, waktu) VALUES ('{request.session['email']}', '{id_song}', current_timestamp);UPDATE song SET total_play = total_play + 1 WHERE id_konten = '{id_song}';")
    return redirect('playlist_detail', id_playlist=id_playlist)