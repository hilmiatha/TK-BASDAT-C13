from django.shortcuts import render

# Create your views here.
def see_chart(request):
    return render(request, 'see_chart.html')


def see_songs_chart(request):
    return render(request, 'see_songs_chart.html')

def see_chart(request):
    context = {
        'is_logged_in' : True,
        'user_type_info'  : {
            'is_pengguna_biasa' : True,
            'is_premium' : True,
            'is_label' : False,
            'is_podcaster' : False,
            'is_artist' : True,
            'is_songwriter' : False,
        },  
    }
    return render(request, 'see_chart.html',context)

def see_songs_chart(request):
    context = {
        'is_logged_in' : True,
        'user_type_info'  : {
            'is_pengguna_biasa' : True,
            'is_premium' : True,
            'is_label' : False,
            'is_podcaster' : False,
            'is_artist' : True,
            'is_songwriter' : False,
        },  
    }
    return render(request, 'see_songs_chart.html',context)