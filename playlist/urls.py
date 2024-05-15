from django.urls import path
from .views import *

urlpatterns = [
    path('', show_playlist, name='show_playlist'),
    path('buat_playlist/', buat_playlist, name='buat_playlist'),
    path('playlist_detail/<uuid:id_playlist>/', playlist_detail, name='playlist_detail'),
    path('tambah_lagu_to_playlist/<uuid:id_playlist>/', tambah_lagu_to_playlist, name='tambah_lagu_to_playlist'),
    path('ubah_playlist/<uuid:id_playlist>/', show_ubah_playlist, name='ubah_playlist'),
    path('hapus_playlist/<uuid:id_playlist>/', hapus_playlist, name='hapus_playlist'),
    path('show_song/<uuid:id_song>/', show_song_detailed, name='show_song'),
    path('add_song_to_playlist/<uuid:id_song>', add_song_to_playlist, name='add_song_to_playlist'),
]