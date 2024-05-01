from django.shortcuts import render

# Create your views here.
def see_chart(request):
    return render(request, 'see_chart.html')


def see_songs_chart(request):
    return render(request, 'see_songs_chart.html')