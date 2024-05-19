from django.http import JsonResponse
from django.shortcuts import render
from utils import parse
from django.db import connection, DatabaseError, transaction
from .query import *
from datetime import datetime
from uuid import uuid4

# Create your views here.
def langganan_paket(request):
    cursor = connection.cursor()
    cursor.execute(get_all_paket())
    result = parse(cursor)

    for row in result:
        row['harga'] = f"Rp{row['harga']:,.0f}".replace(",", ".")

    context = {
        'semua_paket' : result,
    }

    return render(request, 'langganan_paket.html', context)

def pembayaran_paket(request, jenis):
    cursor = connection.cursor()
    cursor.execute(get_paket(jenis))
    result = parse(cursor)

    for row in result:
        row['harga'] = f"Rp{row['harga']:,.0f}".replace(",", ".")

    metode_bayar = ['Transfer Bank', 'Credit Card', 'E-Wallet']

    context = {
        'paket' : result,
        'metode_bayar' : metode_bayar
    }

    return render(request, 'pembayaran_paket.html', context)

def riwayat_paket(request):
    cursor = connection.cursor()
    cursor.execute(get_riwayat_transaksi(request.session['email']))
    result = parse(cursor)

    for row in result:
        row['nominal'] = f"Rp{row['nominal']:,.0f}".replace(",", ".")

    context = {
        'riwayat_transaksi' : result 
    }
    
    return render(request, 'riwayat_paket.html', context)

def pay_paket(request):
    if request.method == 'POST':
        jenis = request.POST.get('jenis')
        metode_bayar = request.POST.get('metode_bayar')
        try:
            cursor = connection.cursor()

            id_transaksi = str(uuid4())
            timestamp_dimulai = datetime.now()
            timestamp_berakhir = timestamp_dimulai
            nominal = 0
            if jenis == '1 bulan':
                cursor.execute(add_one_month())
                timestamp_berakhir = cursor.fetchone()[0]
                cursor.execute(get_harga_one_month())
                nominal = cursor.fetchone()[0]
            elif jenis == '3 bulan':
                cursor.execute(add_three_month())
                timestamp_berakhir = cursor.fetchone()[0]
                cursor.execute(get_harga_three_month())
                nominal = cursor.fetchone()[0]
            elif jenis == '6 bulan':
                cursor.execute(add_six_month())
                timestamp_berakhir = cursor.fetchone()[0]
                cursor.execute(get_harga_six_month())
                nominal = cursor.fetchone()[0]
            else:
                cursor.execute(add_one_year())
                timestamp_berakhir = cursor.fetchone()[0]
                cursor.execute(get_harga_one_year())
                nominal = cursor.fetchone()[0]
            
            cursor.execute(create_transaction(id_transaksi, jenis, request.session['email'], timestamp_dimulai, timestamp_berakhir, metode_bayar, nominal))
            connection.commit()
            request.session['is_premium'] = True
            return JsonResponse({'success': True, 'message': 'Pembelian paket berhasil'})
        except DatabaseError as e:
            connection.rollback()
            return JsonResponse({'success': False, 'message': 'Pembelian paket gagal. Anda sedang memiliki paket yang aktif.'})

