from django.db import connection
from utils import parse
from uuid import uuid4

def delete_album_by_id():
    return f"""
        DELETE FROM ALBUM
        WHERE id = %s;
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

def get_songwriter_by_email():
    return """
        SELECT * FROM SONGWRITER
        WHERE email_akun = %s
    """

def get_id_song_by_songwriter():
    return """
        SELECT * FROM SONGWRITER_WRITE_SONG
        WHERE id_songwriter = %s
    """
    
def get_song_by_id_konten():
    return """
        SELECT * FROM SONG
        WHERE id_konten = %s
    """

def get_label_by_email():
    return """
        SELECT * FROM LABEL
        WHERE email = %s
    """

def get_album_by_id_label():
    return """
        SELECT * FROM ALBUM
        WHERE id_label = %s
    """

def get_song_by_id_album():
    return """
        SELECT * FROM SONG
        WHERE id_album = %s
    """

def get_album_by_id_label():
    return """
        SELECT A.*
        FROM ALBUM A
        JOIN LABEL L ON L.id = A.id_label
        WHERE L.id = %s 
    """

def get_label_by_email():
    return """
        SELECT * 
        FROM LABEL
        WHERE email = %s
    """

def get_song_konten_by_id_album():
    return """
        SELECT S.*, K.*
        FROM SONG S
        JOIN KONTEN K ON S.id_konten = K.id
        WHERE S.id_album = %s
    """