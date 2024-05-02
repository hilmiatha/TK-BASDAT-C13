from django.shortcuts import render

# Create your views here.
def downloaded_songs(request):
    return render(request, 'downloaded_songs.html')