from django.urls import path
from .views import *

urlpatterns = [
   path('hasil_pencarian/', hasil_pencarian, name='hasil_pencarian'),
   path('tidak_ditemukan/', tidak_ditemukan, name='tidak_ditemukan'),
]