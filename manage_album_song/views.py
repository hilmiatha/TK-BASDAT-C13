from django.shortcuts import render

# Create your views here.
def album(request):
    return render(request, 'album.html')

def song(request):
    return render(request, 'songs.html')

def album(request):
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
    return render(request, 'album.html',context)

def songs(request):
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
    return render(request, 'songs.html',context)