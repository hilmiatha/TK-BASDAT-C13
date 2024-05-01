from django.urls import path
from .views import *
urlpatterns = [
    path('test/', test_view, name='test'),
    path('manage_podcast/', manage_podcast, name='manage_podcast'),
     path('manage_episode/', manage_episode, name='manage_episode'),
]