from django.urls import path
from .views import *

urlpatterns = [
   path('see_chart/', see_chart, name='see_chart'),
   path('see_songs_chart/<uuid:id_playlist>/', see_songs_chart, name='see_songs_chart')
]