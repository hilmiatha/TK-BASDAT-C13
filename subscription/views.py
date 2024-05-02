from django.shortcuts import render

# Create your views here.
def langganan_paket(request):
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
    return render(request, 'langganan_paket.html',context)

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