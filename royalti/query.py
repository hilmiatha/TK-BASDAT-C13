from django.db import connection
from utils import parse
from uuid import uuid4


def get_all_labels():
    return f"SELECT * FROM LABEL"

def get_all_albums():
    return """
        SELECT A.*, L.nama AS label_name
        FROM ALBUM A
        JOIN LABEL L ON A.id_label = L.id
    """

def get_all_artists():
    return """
        SELECT AR.*, AK.nama AS akun_name FROM ARTIST AR
        JOIN AKUN AK ON AK.email = AR.email_akun
    """

def get_all_songwriters():
    return """
        SELECT S.*, AK.nama AS akun_name FROM SONGWRITER S
        JOIN AKUN AK ON AK.email = S.email_akun
    """

def get_all_genres():
    return """
        SELECT G.*, K.* FROM GENRE G
        JOIN KONTEN K ON K.id = G.id_konten
    """

def get_all_songs():
    return """
        SELECT * FROM SONG
    """

def create_album():
    return """
        INSERT INTO ALBUM (id, judul, id_label)
        VALUES (%s, %s, %s);
    """

def delete_album_by_id():
    return f"""
        DELETE FROM ALBUM
        WHERE id = %s;
    """

def create_song():
    return """
        INSERT INTO SONG (id_konten, id_artist, id_album)
        VALUES (%s, %s, %s)
    """

def assign_songwriter():
    return """
        INSERT INTO SONGWRITER_WRITE_SONG (id_songwriter, id_song)
        VALUES (%s, %s)
    """

def create_konten():
    return """
        INSERT INTO KONTEN (id, judul, tanggal_rilis, tahun, durasi)
        VALUES (%s, %s, %s, %s, %s)
    """

def get_song_by_id_artist():
    return """  
        SELECT * 
        FROM SONG
        WHERE id_artist = %s
    """

def get_artist_by_email():
    return """
        SELECT *
        FROM ARTIST
        WHERE email_akun = %s
    """

def get_konten_by_id_konten():
    return """
        SELECT *
        FROM KONTEN
        WHERE id = %s
    """

def get_album_by_id_album():
    return """
        SELECT *
        FROM ALBUM 
        WHERE id = %s
    """

def get_song_konten_album_by_id_artist():
    return """
        SELECT SONG.*, KONTEN.*, ALBUM.*
        FROM SONG
        JOIN KONTEN ON SONG.id_konten = KONTEN.id
        JOIN ALBUM ON SONG.id_album = ALBUM.id
        WHERE SONG.id_artist = %s
    """

def get_pemilik_hak_cipta_by_id():
    return """
        SELECT * FROM PEMILIK_HAK_CIPTA
        WHERE id = %s
    """

def create_royalti():
    return """ 
        INSERT INTO ROYALTI (id_pemilik_hak_cipta, id_song, jumlah)
        VALUES (%s, %s, %s)
        ON CONFLICT (id_pemilik_hak_cipta, id_song)
        DO UPDATE SET jumlah = EXCLUDED.jumlah
    """

def get_royalti_by_id():
    return """
        SELECT * FROM ROYALTI
        WHERE id_pemilik_hak_cipta = %s AND id_song = %s
    """