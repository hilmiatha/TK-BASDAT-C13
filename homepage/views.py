from django.shortcuts import render
from django.db import connection
from homepage.query import *
from utils import parse
from django.views.decorators.csrf import csrf_exempt


def homepage_view(request):
    return render(request, 'homepage.html')

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