from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage_view, name='homepage'),
    path('login/', show_login, name='show_login'),
    path('register/', show_register, name='show_register'),
    path('register/show_register_pengguna/', show_register_pengguna, name='show_register_pengguna'),
    path('register/show_register_label/', show_register_label, name='show_register_label'),
]