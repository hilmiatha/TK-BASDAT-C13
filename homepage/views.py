from uuid import uuid4
from django.shortcuts import redirect, render
from django.db import connection
from homepage.query import *
from utils import parse
from django.views.decorators.csrf import csrf_exempt


def homepage_view(request):
    # context = {
    #     'is_logged_in' : False,
    #     'user_type_info'  : {
    #         'is_pengguna_biasa' : False,
    #         'is_premium' : False,
    #         'is_label' : False,
    #         'is_podcaster' : False,
    #         'is_artist' : False,
    #         'is_songwriter' : False,
    #     },  
    # }
    return render(request, 'homepage.html')


@csrf_exempt
def show_login(request):
    if request.method == 'POST':
        pw = request.POST.get('password')
        email = request.POST.get('email')
        cursor = connection.cursor()
        cursor.execute(cek_user(email, pw))
        res = parse(cursor)
        if len(res) == 0:
            return render(request, 'login.html', {'error_message': 'Email atau password salah'})
        else:
            request.session['email'] = email
            request.session['is_pengguna_biasa'] = True
            request.session['is_premium'] = False
            request.session['is_label'] = False
            request.session['is_podcaster'] = False
            request.session['is_artist'] = False
            request.session['is_songwriter'] = False
            
            cursor.execute(cek_premium(email))
            if len(parse(cursor)) > 0:
                request.session['is_premium'] = True
                
            cursor.execute(cek_label(email))
            if len(parse(cursor)) > 0:
                request.session['is_label'] = True
            
            cursor.execute(cek_podcaster(email))
            if len(parse(cursor)) > 0:
                request.session['is_podcaster'] = True
                
            cursor.execute(cek_artist(email))
            if len(parse(cursor)) > 0:
                request.session['is_artist'] = True
            
            cursor.execute(cek_songwriter(email))
            if len(parse(cursor)) > 0:
                request.session['is_songwriter'] = True
            
            return redirect('/dashboard/dashboard')
                
            
    
    return render(request, 'login.html')


@csrf_exempt
def show_register(request):
    return render(request, 'register.html')

@csrf_exempt
def show_register_pengguna(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        birthplace = request.POST.get('birthplace')
        birthdate = request.POST.get('birthdate')
        city = request.POST.get('city')
        gender = 1 if request.POST.get('gender') == 'male' else 0
        role_podcaster = request.POST.get('is_podcaster') == 'podcaster'
        role_artist = request.POST.get('is_artist') == 'artist'
        role_songwriter = request.POST.get('is_songwriter') == 'songwriter'
        
        print(role_podcaster, role_artist, role_songwriter)

        cursor = connection.cursor()

        # Check if the email already exists
        cursor.execute("SELECT email FROM akun WHERE email = %s", [email])
        if cursor.fetchone():
            return render(request, 'register_pengguna.html', {'error_message': 'Email already exists'})
        
        roles = []
        if role_podcaster:
            roles.append('podcaster')
        if role_artist:
            roles.append('artist')
        if role_songwriter:
            roles.append('songwriter')
        
        if roles:
            verification_status = True
        else:
            verification_status = False
        
        # Insert the new user into the database
        cursor.execute(
            "INSERT INTO akun (email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            [email, password, name, gender, birthplace, birthdate, verification_status, city]
        )

        # Determine role and verification status
        if role_podcaster:
            cursor.execute("INSERT INTO podcaster (email) VALUES (%s)", [email])
        if role_artist:
            uuid = str(uuid4())
            cursor.execute("INSERT INTO artist (id, email_akun) VALUES (%s, %s)", [uuid, email])
        if role_songwriter:
            uuid = str(uuid4())
            cursor.execute("INSERT INTO songwriter (id, email_akun) VALUES (%s, %s)", [uuid, email])
        
      
        #insert nonpremium
        cursor.execute("INSERT INTO nonpremium (email) VALUES (%s)", [email])

        
        connection.commit()

        # Set session variables
        request.session['email'] = email
        request.session['is_verified'] = (verification_status == 'Verified')
        request.session['is_premium'] = False
        request.session['is_pengguna_biasa'] = True
        request.session['is_label'] = False
        for role in roles:
            request.session[f'is_{role}'] = True

        return redirect('/dashboard/dashboard')

    return render(request, 'register_pengguna.html')


@csrf_exempt
def show_register_label(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        
        cursor = connection.cursor()

        # Check if the email already exists in the database
        cursor.execute("SELECT * FROM label WHERE email = %s", [email])
        if cursor.fetchone():
            return render(request, 'register_label.html', {'error_message': 'Email already exists'})

        # Insert the new label into the database
        uuid = str(uuid4())
        cursor.execute("INSERT INTO label (id, email, password, nama, kontak) VALUES (%s, %s, %s, %s, %s)", [uuid, email, password, name, contact])
        connection.commit()

        # Automatically log in the label or redirect to login page
        request.session['email'] = email
        request.session['is_pengguna_biasa'] = True
        request.session['is_premium'] = False
        request.session['is_label'] = True
        request.session['is_podcaster'] = False
        request.session['is_artist'] = False
        request.session['is_songwriter'] = False
        return redirect('/dashboard/dashboard')

    return render(request, 'register_label.html')

@csrf_exempt
def logout(request):
    request.session.flush()
    return redirect('homepage')