from django.shortcuts import render

# Create your views here.
def hasil_pencarian(request):
    return render(request, 'hasil_pencarian.html')

def tidak_ditemukan(request):
    return render(request, 'tidak_ditemukan.html')