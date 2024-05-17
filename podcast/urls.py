from django.urls import path
from .views import *
urlpatterns = [
    path('play_podcast/<uuid:id_podcast>/', play_podcast, name='play_podcast'),
    path('manage_podcast/', manage_podcast, name='manage_podcast'),
    path('manage_episode/<uuid:id_podcast>/', manage_episode, name='manage_episode'),
    path('hapus_podcast/<uuid:id_podcast>/', hapus_podcast, name='hapus_podcast'),
    path('hapus_episode/<uuid:id_episode>/', hapus_episode, name='hapus_episode'),
]