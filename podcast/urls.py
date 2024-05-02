from django.urls import path
from .views import *
urlpatterns = [
    path('play_podcast/', play_podcast, name='play_podcast'),
    path('manage_podcast/', manage_podcast, name='manage_podcast'),
     path('manage_episode/', manage_episode, name='manage_episode'),
]