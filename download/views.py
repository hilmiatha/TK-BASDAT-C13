from django.shortcuts import render

# Create your views here.
def downloaded_songs(request):
    context = {
            'is_logged_in' : True,
            'user_type_info'  : {
                'is_pengguna_biasa' : True,
                'is_premium' :  True,
                'is_label' : False,
                'is_podcaster' : False,
                'is_artist' : False,
                'is_songwriter' : False,
            },  
        }
    return render(request, 'downloaded_songs.html',context)