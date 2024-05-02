def get_waktu_jam(a):
    if a < 60:
        return f'{a} menit'
    else:
        return f'{a//60} jam {a%60} menit'