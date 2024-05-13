def get_paket():
    return """SELECT * FROM PAKET;"""

def create_transaction(id_transaksi, jenis_paket, email, timestamp_dimulai, timestamp_berakhir, metode_bayar, nominal):
    return f"""INSERT INTO TRANSACTION VALUES 
    ('{id_transaksi}','{jenis_paket}','{email}','{timestamp_dimulai}','{timestamp_berakhir}','{metode_bayar}',{nominal});"""

def get_riwayat_transaksi(email):
    return f"""SELECT * FROM TRANSACTION WHERE email = '{email}';"""