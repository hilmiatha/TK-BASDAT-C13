from pyexpat.errors import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db import DatabaseError, connection, transaction
from django.urls import reverse
from pyexpat.errors import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db import DatabaseError, connection, transaction
from django.urls import reverse
from .query import *
from utils import parse
from django.views.decorators.csrf import csrf_exempt
from .functions import *
from uuid import uuid4


# Create your views here.
@csrf_exempt
def play_podcast(request, id_podcast):
    cursor = connection.cursor()
    cursor.execute(get_podcast(id_podcast))
    res = parse(cursor)
    cursor.execute(get_episodes(id_podcast))
    res2 = parse(cursor)
    print(len(res))
    res[0]['durasi'] = get_waktu_jam(res[0].get('durasi'))
    print(res[0])
    for i in range(len(res2)):
        res2[i]['durasi'] = get_waktu_jam(res2[i].get('durasi'))
    context = {
        'info_podcast' : res[0],
        'genre' : res[0].get('genre').split(','),
        'episodes' : res2,
    }
    return render(request, 'play_podcast.html',context)

@csrf_exempt
def manage_podcast(request):
    email = request.session['email']
    cursor = connection.cursor()
    cursor.execute(get_genres())
    res = parse(cursor)
    cursor.execute(get_podcasts_list(email))
    res2 = parse(cursor)
    for i in range(len(res2)):
        res2[i]['durasi'] = get_waktu_jam(res2[i].get('durasi'))
    context = {
        'genres' : res,
        'podcasts' : res2
    }

    if request.method == 'POST':
        judul = request.POST.get('judul')
        genres = request.POST.getlist('genre')
        uuid_podcast = str(uuid4())
        try:
            with transaction.atomic():
               cursor.execute(make_podcast(email, judul, uuid_podcast))
               for i in range(len(genres)):
                   cursor.execute(add_genre(uuid_podcast, genres[i]))

            return redirect('manage_podcast')
            
        except DatabaseError as e:
            if 'Podcast sudah ada dalam sistem' in str(e):
                context['error_message'] = 'Lagu sudah ada dalam playlist'

            return redirect('manage_podcast')


    return render(request, 'manage_podcast.html', context)

@csrf_exempt
def manage_episode(request, id_podcast):
    cursor = connection.cursor()
    cursor.execute(get_podcast(id_podcast))
    res = parse(cursor)
    cursor.execute(get_episodes(id_podcast))
    res2 = parse(cursor)
    res[0]['durasi'] = get_waktu_jam(res[0].get('durasi'))
    for i in range(len(res2)):
        res2[i]['durasi'] = get_waktu_jam(res2[i].get('durasi'))
    context = {
        'podcast' : res[0],
        'id' : id_podcast,
        'episodes' : res2
    }

    if request.method == 'POST':
        judul = request.POST.get('judul')
        deskripsi = request.POST.get('deskripsi')
        durasi = request.POST.get('durasi')
        uuid_episode = str(uuid4())
        
        try:
            with transaction.atomic():
                cursor.execute(make_episode(uuid_episode, id_podcast, judul, deskripsi, durasi))
            return redirect('manage_episode', id_podcast=id_podcast)

        except DatabaseError as e:
            if 'Episode sudah ada dalam podcast' in str(e):
                context['error_message'] = 'Episode sudah ada dalam podcast'
            return redirect('manage_episode', id_podcast=id_podcast)
        
    return render(request, 'manage_episode.html', context)

@csrf_exempt
def hapus_podcast(request, id_podcast):
    cursor = connection.cursor()
    cursor.execute(delete_podcast(id_podcast))
    connection.commit()
    return redirect('manage_podcast')

@csrf_exempt
def hapus_episode(request, id_episode):
    cursor = connection.cursor()
    cursor.execute(get_id_podcast(id_episode))
    res = parse(cursor)
    cursor.execute(delete_episode(id_episode))
    connection.commit()
    return redirect('manage_episode', id_podcast=res[0].get('id'))