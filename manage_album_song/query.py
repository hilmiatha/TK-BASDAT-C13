from django.db import connection
from utils import parse
from uuid import uuid4
import datetime


def get_all_labels():
    return f"SELECT * FROM LABEL"

def get_all_akuns():
    return f"""SELECT * FROM LABEL
    """

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
        SELECT DISTINCT *
        FROM GENRE
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

def delete_song_by_id():
    return f"""
        DELETE FROM SONG
        WHERE id_konten = %s;
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

def get_akun_by_email():
    return """
        SELECT * FROM AKUN
        WHERE email = %s
    """

def create_konten():
    return """
        INSERT INTO KONTEN (id, judul, tanggal_rilis, tahun, durasi)
        VALUES (%s, %s, %s, %s, %s)
    """

def get_album_by_id():
    return """
        SELECT * FROM ALBUM
        WHERE id = %s
    """

def get_song_konten_by_id_album():
    return """
        SELECT S.*, K.*
        FROM SONG S
        JOIN KONTEN K ON S.id_konten = K.id
        WHERE S.id_album = %s
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

def get_album_by_artist():
    return """
        SELECT DISTINCT A.*
        FROM ALBUM A
        JOIN SONG S ON S.id_album = A.id
        JOIN ARTIST AR ON AR.id = S.id_artist
        WHERE AR.email_akun = %s
    """

def get_album_by_songwriter():
    return """
        SELECT DISTINCT A.*
        FROM ALBUM A
        JOIN SONG S ON S.id_album = A.id
        JOIN SONGWRITER_WRITE_SONG SWS ON SWS.id_song = S.id_konten 
        JOIN SONGWRITER SW ON SW.id = SWS.id_songwriter
        WHERE SW.email_akun = %s
    """

def get_artist_by_email():
    return """
        SELECT AK.*, A.*
        FROM AKUN AK
        JOIN ARTIST A ON AK.email = A.email_akun
        WHERE email=%s
    """

def get_songwriter_by_email():
    return """
        SELECT AK.*, SW.*
        FROM AKUN AK
        JOIN SONGWRITER SW ON AK.email = SW.email_akun
        WHERE email=%s
    """

def insert_genre_to_song():
    return """
        INSERT INTO GENRE (id_konten, genre)
        VALUES (%s, %s)
    """

def insert_song(judul, durasi, id_artist, id_album, songwriters, genres):
    cursor = connection.cursor()
    uuid_konten = str(uuid4())
    current_date = datetime.date.today()
    cursor.execute(create_konten(), [uuid_konten, judul, current_date, current_, durasi])

    cursor.execute(create_song(), [uuid_konten, id_artist, id_album])

    for genre in genres:
        cursor.execute(insert_genre_to_song(), [uuid_konten, genre])

    for id_songwriter in songwriters:
        cursor.execute(assign_songwriter(), [id_songwriter, uuid_konten])