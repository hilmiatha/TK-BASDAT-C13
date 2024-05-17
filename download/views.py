from django.db import connection
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from utils import parse
from .query import *

# Create your views here.
def downloaded_songs(request):
    cursor = connection.cursor()
    cursor.execute(get_downloaded_songs(request.session['email']))
    result = parse(cursor)
    context = {
        'downloaded_songs' : result
    }

    return render(request, 'downloaded_songs.html',context)

def delete_downloaded_song(request, id_song, email_downloader):
    if request.method == 'POST':
        cursor = connection.cursor()
        cursor.execute(delete_downloaded_song_query(id_song, email_downloader))
        connection.commit()
        cursor.execute(get_song_name(id_song))
        deleted_song_name = parse(cursor)
        return JsonResponse({'success': True, 'message': f"Berhasil menghapus lagu dengan judul '{deleted_song_name[0].get('judul')}' dari daftar unduhan!"})
