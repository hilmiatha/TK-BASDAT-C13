from uuid import uuid4
import datetime

def get_podcast(id_podcast):
    return f"""
    SELECT 
        K.judul AS judul,
        string_agg(G.genre, ',') AS genre,
        A.nama AS nama,
        K.durasi AS durasi,
        K.tanggal_rilis AS tanggal_rilis,
        K.tahun AS tahun
    FROM 
        PODCAST AS P
        JOIN KONTEN AS K ON K.id = P.id_konten
        LEFT JOIN PODCASTER AS PR ON P.email_podcaster = PR.email
        LEFT JOIN GENRE AS G ON G.id_konten = P.id_konten
        LEFT JOIN AKUN AS A ON A.email = PR.email
    WHERE 
        P.id_konten = '{id_podcast}'
    GROUP BY
        K.judul, A.nama, K.durasi, K.tanggal_rilis, K.tahun;
    """

def get_episodes(id_podcast):
    return f"""
    SELECT 
            id_episode AS id, judul, deskripsi, durasi, tanggal_rilis as tanggal
        FROM
            EPISODE
        WHERE
            id_konten_podcast = '{id_podcast}';
    """

def get_genres():
    return f"""
    SELECT DISTINCT genre
    FROM genre;
    """

def get_podcasts_list(email_podcaster):
    return f"""
    SELECT DISTINCT 
        P.id_konten as id,
        K.judul as judul,
        COALESCE((SELECT COUNT(*) 
                  FROM EPISODE 
                  WHERE EPISODE.id_konten_podcast = P.id_konten), 0) AS jumlah_episode,
        K.durasi as durasi
    FROM
        PODCAST AS P
        JOIN KONTEN AS K ON K.id = P.id_konten
        LEFT JOIN EPISODE AS E ON E.id_konten_podcast = P.id_konten
    WHERE
        P.email_podcaster = '{email_podcaster}'
    ORDER BY 
        K.judul;
    """

# Nambah ke podcast, konten, genre
def make_podcast(email_podcaster ,judul, uuid_podcast):
    current_date = datetime.date.today()
    return f"""
    INSERT INTO KONTEN (id, judul, tanggal_rilis, tahun, durasi)
    VALUES ('{uuid_podcast}', '{judul}', '{current_date}' , '{current_date.year}', 0);
    
    INSERT INTO PODCAST (id_konten, email_podcaster)
    VALUES ('{uuid_podcast}', '{email_podcaster}');
    """

def add_genre(id_konten, genre):
    return f"""
    INSERT INTO GENRE (id_konten, genre)
    VALUES ('{id_konten}', '{genre}');
    """

# DURASI MASI NGACO COK
def make_episode(uuid_episode, uuid_podcast, judul, deskripsi, durasi):
    current_date = datetime.date.today()
    return f"""
    INSERT INTO EPISODE (id_episode, id_konten_podcast, judul, deskripsi, durasi, tanggal_rilis)
    VALUES ('{uuid_episode}', '{uuid_podcast}', '{judul}', '{deskripsi}', '{durasi}', '{current_date}');
    """

def delete_podcast(id_podcast):
    return f"""
    DELETE 
    FROM KONTEN 
    WHERE id = '{id_podcast}';
    """

def delete_episode(id_episode):
    return f"""
    DELETE
    FROM EPISODE
    WHERE id_episode = '{id_episode}';
    """

def get_id_podcast(id_episode):
    return f"""
    SELECT id_konten_podcast as id
    FROM EPISODE
    WHERE id_episode = '{id_episode}';
    """