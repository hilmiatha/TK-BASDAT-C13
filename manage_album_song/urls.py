from django.urls import path
from .views import *

urlpatterns = [
    path('album/', album, name='album'),
    path('songs/<str:id>', songs, name='songs'),
    path('delete-album/<str:id>', delete_album, name='delete_album'),
    path('delete-song/<str:id>', delete_song, name='delete_song'),
]