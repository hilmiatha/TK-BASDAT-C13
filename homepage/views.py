from uuid import uuid4
from django.shortcuts import redirect, render
from django.db import DatabaseError, IntegrityError, connection
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
        if not pw or not email:
            return render(request, 'login.html', {'error_message': 'Email atau password tidak boleh kosong'})
        cursor = connection.cursor()
        cursor.execute(cek_user(email, pw))
        res = parse(cursor)
        cursor.execute(cek_label(email, pw))
        res2 = parse(cursor)
        cursor.execute("CALL check_and_update_subscription_status(%s)", [email])
        if len(res) == 0 and len(res2) == 0:
            return render(request, 'login.html', {'error_message': 'Email atau password salah'})
        elif len(res) >= 1:
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
        else:
            cursor.execute(cek_label(email, pw))
            if len(parse(cursor))  == 0:
                return render(request, 'login.html', {'error_message': 'Email atau password salah'})
            else:
                request.session['email'] = email
                request.session['is_pengguna_biasa'] = False
                request.session['is_premium'] = False
                request.session['is_label'] = True
                request.session['is_podcaster'] = False
                request.session['is_artist'] = False
                request.session['is_songwriter'] = False
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
        if not password or not email or not name or not birthplace or not birthdate or not city:
            return render(request, 'register_pengguna.html', {'error_message': 'Field tidak boleh kosong'})
        
        roles = []
        if role_podcaster:
            roles.append('podcaster')
        if role_artist:
            roles.append('artist')
        if role_songwriter:
            roles.append('songwriter')
        
        verification_status = bool(roles)
        
        cursor = connection.cursor()

        try:
            # Insert the new user into the database
            cursor.execute(
                "INSERT INTO akun (email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                [email, password, name, gender, birthplace, birthdate, verification_status, city]
            )

            # Determine role and verification status
            if role_podcaster:
                cursor.execute("INSERT INTO podcaster (email) VALUES (%s)", [email])
                request.session['is_podcaster'] = True
            else:
                request.session['is_podcaster'] = False
            if role_artist:
                uuid = str(uuid4())
                cursor.execute("INSERT INTO artist (id, email_akun) VALUES (%s, %s)", [uuid, email])
                request.session['is_artist'] = True
            else:
                request.session['is_artist'] = False
            if role_songwriter:
                uuid = str(uuid4())
                cursor.execute("INSERT INTO songwriter (id, email_akun) VALUES (%s, %s)", [uuid, email])
                request.session['is_songwriter'] = True
            else:
                request.session['is_songwriter'] = False
            
            connection.commit()

        except DatabaseError as e: 
            # Handle the email already exists exception
            if (f'Email {email} already exists!' in str(e) ):
                return render(request, 'register_pengguna.html', {'error_message': 'Email already exists'})
        
        uuid_hak_cipta = str(uuid4())
        rate_royalti = 50000
        cursor.execute("INSERT INTO pemilik_hak_cipta (id, rate_royalti) VALUES (%s, %s)", [uuid_hak_cipta, rate_royalti])
        
        
        if role_artist:
            cursor.execute("UPDATE artist SET id_pemilik_hak_cipta = %s WHERE email_akun = %s", [uuid_hak_cipta, email])
        if role_songwriter:
            cursor.execute("UPDATE songwriter SET id_pemilik_hak_cipta = %s WHERE email_akun = %s", [uuid_hak_cipta, email])

        # Set session variables
        request.session['email'] = email
        request.session['is_verified'] = verification_status
        request.session['is_premium'] = False
        request.session['is_pengguna_biasa'] = True
        request.session['is_label'] = False
        

        return redirect('/dashboard/dashboard')

    return render(request, 'register_pengguna.html')


@csrf_exempt
def show_register_label(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        if not password or not email or not name or not name or not contact:
            return render(request, 'register_label.html', {'error_message': 'Field tidak boleh kosong'})
        
        cursor = connection.cursor()

        try:
            # Insert the new label into the database
            uuid = str(uuid4())
            cursor.execute("INSERT INTO label (id, email, password, nama, kontak) VALUES (%s, %s, %s, %s, %s)", [uuid, email, password, name, contact])
            connection.commit()

        except DatabaseError as e:
            # Handle the email already exists exception
            if (f'Email {email} already exists!' in str(e) ):
                return render(request, 'register_label.html', {'error_message': 'Email already exists'})
        
        uuid_hak_cipta = str(uuid4())
        rate_royalti = 50000
        cursor.execute("INSERT INTO pemilik_hak_cipta (id, rate_royalti) VALUES (%s, %s)", [uuid_hak_cipta, rate_royalti])
        cursor.execute("UPDATE label SET id_pemilik_hak_cipta = %s WHERE id = %s", [uuid_hak_cipta, uuid])

        # Automatically log in the label or redirect to login page
        request.session['email'] = email
        request.session['is_pengguna_biasa'] = False
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