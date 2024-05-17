from django.urls import path
from .views import *

urlpatterns = [
   path('downloaded_songs/', downloaded_songs, name='downloaded_songs'),
   path('delete_downloaded_song/<uuid:id_song>/<str:email_downloader>', delete_downloaded_song, name='delete_downloaded_song')
]