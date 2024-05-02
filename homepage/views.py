from django.shortcuts import render
from django.db import connection
from homepage.query import *
from utils import parse
from django.views.decorators.csrf import csrf_exempt


def homepage_view(request):
    context = {
        'is_logged_in' : False,
        'user_type_info'  : {
            'is_pengguna_biasa' : False,
            'is_premium' : False,
            'is_label' : False,
            'is_podcaster' : False,
            'is_artist' : False,
            'is_songwriter' : False,
        },  
    }
    return render(request, 'homepage.html', context)


@csrf_exempt
def show_login(request):
    return render(request, 'login.html')


@csrf_exempt
def show_register(request):
    return render(request, 'register.html')

@csrf_exempt
def show_register_pengguna(request):
    return render(request, 'register_pengguna.html')


@csrf_exempt
def show_register_label(request):
    return render(request, 'register_label.html')