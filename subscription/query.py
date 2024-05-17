def get_all_paket():
    return """SELECT * FROM PAKET;"""

def get_paket(jenis):
    return f"""SELECT * FROM PAKET WHERE jenis = '{jenis}';"""

def create_transaction(id_transaksi, jenis_paket, email, timestamp_dimulai, timestamp_berakhir, metode_bayar, nominal):
    return f"""INSERT INTO TRANSACTION VALUES 
    ('{id_transaksi}','{jenis_paket}','{email}','{timestamp_dimulai}','{timestamp_berakhir}','{metode_bayar}',{nominal});"""

def get_riwayat_transaksi(email):
    return f"""SELECT * FROM TRANSACTION WHERE email = '{email}';"""

def add_one_month():
    return """SELECT NOW() + INTERVAL '1 month'"""

def add_three_month():
    return """SELECT NOW() + INTERVAL '3 months'"""

def add_six_month():
    return """SELECT NOW() + INTERVAL '6 months'"""

def add_one_year():
    return """SELECT NOW() + INTERVAL '1 year'"""

def get_harga_one_month():
    return """SELECT harga FROM PAKET WHERE jenis = '1 bulan';"""

def get_harga_three_month():
    return """SELECT harga FROM PAKET WHERE jenis = '3 bulan';"""

def get_harga_six_month():
    return """SELECT harga FROM PAKET WHERE jenis = '6 bulan';"""

def get_harga_one_year():
    return """SELECT harga FROM PAKET WHERE jenis = '1 tahun';"""