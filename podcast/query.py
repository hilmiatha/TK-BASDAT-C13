from uuid import uuid4

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
        JOIN PODCASTER AS PR ON P.email_podcaster = PR.email
        JOIN GENRE AS G ON G.id_konten = P.id_konten
        JOIN AKUN AS A ON A.email = PR.email    
    WHERE 
        P.id_konten = '{id_podcast}'
    GROUP BY
        K.judul, A.nama, K.durasi, K.tanggal_rilis, K.tahun;
    """

def get_episodes(id_podcast):
    return f"""
    SELECT 
            judul, deskripsi, durasi, tanggal_rilis as tanggal
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
        (SELECT COUNT(*) 
            FROM EPISODE 
            WHERE EPISODE.id_konten_podcast = P.id_konten) AS jumlah_episode,
        K.durasi as durasi
    FROM
        PODCAST AS P
        JOIN KONTEN AS K ON K.id = P.id_konten
        JOIN EPISODE AS E ON E.id_konten_podcast = P.id_konten
    WHERE
        P.email_podcaster = '{email_podcaster}'
    ORDER BY 
        K.judul;
    """

# Nambah ke podcast, konten, genre
def make_podcast(email_podcaster ,judul, genres):
    uuid_podcast = str(uuid4())
    return f"""
    INSERT INTO PODCAST (id_konten, email_podcaster)
    VALUES ('{uuid_podcast}', '{email_podcaster}');

    INSERT INTO 
    """
