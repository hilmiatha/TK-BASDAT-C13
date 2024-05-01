from django.shortcuts import render

# Create your views here.
def check_royalti(request):
    return render(request, 'check_royalti.html')

def list_album(request):
    return render(request, 'list_album.html')

def list_song(request):
    return render(request, 'list_song.html')