from django.shortcuts import render

# Create your views here.
def langganan_paket(request):
    return render(request, 'langganan_paket.html')

def pembayaran_paket(request):
    return render(request, 'pembayaran_paket.html')

def riwayat_paket(request):
    return render(request, 'riwayat_paket.html')