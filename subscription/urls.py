from django.urls import path
from .views import *

urlpatterns = [
   path('langganan_paket', langganan_paket, name='langganan_paket'),
   path('pembayaran_paket/<str:jenis>/', pembayaran_paket, name='pembayaran_paket'),
   path('riwayat_paket', riwayat_paket, name='riwayat_paket'),
   path('pay_paket', pay_paket, name='pay_paket'),
]