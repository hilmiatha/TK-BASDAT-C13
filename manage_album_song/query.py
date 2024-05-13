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

def insert_song(judul, durasi, id_artist, id_album, songwriters):
    cursor = connection.cursor()
    uuid_konten = str(uuid4())
    current_date = datetime.date.today()
    cursor.execute(create_konten(), [uuid_konten, judul, current_date, current_date.year, durasi])

    cursor.execute(create_song(), [uuid_konten, id_artist, id_album])

    for id_songwriter in songwriters:
        cursor.execute(assign_songwriter(), [id_songwriter, uuid_konten])