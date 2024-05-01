from django.urls import path
from .views import *

urlpatterns = [
   path('check_royalti/', check_royalti, name='check_royalti'),
   path('list_album/', list_album, name='list_album'),
   path('list_song/', list_song, name='list_song')
]