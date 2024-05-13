from django.urls import path
from .views import *

urlpatterns = [
    path('album/', album, name='album'),
    path('songs/', songs, name='songs'),
    path('delete-album/<str:id>', delete_album, name='delete_album')
]