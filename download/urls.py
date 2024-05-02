from django.urls import path
from .views import *

urlpatterns = [
   path('downloaded_songs/', downloaded_songs, name='downloaded_songs'),
]