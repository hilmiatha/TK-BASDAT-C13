def get_waktu_jam(a):
    if a < 60:
        return f'{a} menit'
    elif a % 60 == 0:
        return f'{a//60} jam'
    else:
        return f'{a//60} jam {a%60} menit'