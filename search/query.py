def search_query_song(query_input):
    return f"""SELECT K.judul, A.nama, K.id FROM SONG S, ARTIST AR, AKUN A, KONTEN K 
    WHERE S.id_konten = K.id 
    AND S.id_artist = AR.id 
    AND AR.email_akun = A.email 
    AND K.judul ILIKE '%{query_input}%';"""

def search_query_podcast(query_input):
    return f"""SELECT K.judul, A.nama, K.id FROM PODCAST P, AKUN A, KONTEN K 
    WHERE P.id_konten = K.id 
    AND P.email_podcaster = A.email
   and K.judul ILIKE '%{query_input}%';"""

def search_query_user_playlist(query_input):
    return f"""SELECT UP.judul, A.nama, UP.id_playlist FROM USER_PLAYLIST UP, AKUN A
    WHERE UP.email_pembuat = A.email and UP.judul ilike '%{query_input}%';"""