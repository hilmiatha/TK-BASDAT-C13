from django.shortcuts import render

# Create your views here.
def check_royalti(request):
    return render(request, 'check_royalti.html')

def list_album(request):
    return render(request, 'list_album.html')

def list_song(request):
    return render(request, 'list_song.html')

def check_royalti(request):
    context = {
        'is_logged_in' : True,
        'user_type_info'  : {
            'is_pengguna_biasa' : False,
            'is_premium' : False,
            'is_label' : True,
            'is_podcaster' : False,
            'is_artist' : False,
            'is_songwriter' : False,
        },  
    }
    return render(request, 'check_royalti.html',context)

def list_album(request):
    context = {
        'is_logged_in' : True,
        'user_type_info'  : {
            'is_pengguna_biasa' : False,
            'is_premium' : False,
            'is_label' : False,
            'is_podcaster' : False,
            'is_artist' : True,
            'is_songwriter' : False,
        },  
    }
    return render(request, 'list_album.html',context)

def list_song(request):
    context = {
        'is_logged_in' : True,
        'user_type_info'  : {
            'is_pengguna_biasa' : False,
            'is_premium' : False,
            'is_label' : False,
            'is_podcaster' : False,
            'is_artist' : True,
            'is_songwriter' : False,
        },  
    }
    return render(request, 'list_song.html',context)