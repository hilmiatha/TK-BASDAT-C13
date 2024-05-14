from django.shortcuts import render
from utils import parse
from django.db import connection
from .query import *

# Create your views here.
def langganan_paket(request):
    cursor = connection.cursor()
    cursor.execute(get_paket())
    result = parse(cursor)

    for row in result:
        row['harga'] = format_harga(row['harga'])
    
    print(result)

    context = {
        'is_logged_in' : True,
        'semua_paket' : result,
        'user_type_info'  : {
            'is_pengguna_biasa' : True,
            'is_premium' : False,
            'is_label' : False,
            'is_podcaster' : False,
            'is_artist' : False,
            'is_songwriter' : False,
        },  
    }
    return render(request, 'langganan_paket.html',context)

def format_harga(harga):
    return f"Rp{harga:,.0f}".replace(",", ".")

def pembayaran_paket(request):
    context = {
        'is_logged_in' : True,
        'user_type_info'  : {
            'is_pengguna_biasa' : True,
            'is_premium' : False,
            'is_label' : False,
            'is_podcaster' : False,
            'is_artist' : False,
            'is_songwriter' : False,
        },  
    }
    return render(request, 'pembayaran_paket.html',context)

def riwayat_paket(request):
    context = {
        'is_logged_in' : True,
        'user_type_info'  : {
            'is_pengguna_biasa' : True,
            'is_premium' : False,
            'is_label' : False,
            'is_podcaster' : False,
            'is_artist' : False,
            'is_songwriter' : False,
        },  
    }
    return render(request, 'riwayat_paket.html',context)