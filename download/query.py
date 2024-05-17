def get_downloaded_songs(email):
    return f"""SELECT K.judul, A.nama, K.id, DS.email_downloader, DS.email_downloader FROM DOWNLOADED_SONG DS, SONG S, ARTIST AR, KONTEN K, AKUN A 
    WHERE DS.email_downloader = '{email}' 
    AND DS.id_song = S.id_konten 
    AND S.id_konten = K.id 
    AND S.id_artist = AR.id 
    AND AR.email_akun = A.email;"""

def delete_downloaded_song_query(id_song, email_downloader):
    return f"""DELETE FROM DOWNLOADED_SONG WHERE id_song = '{id_song}' AND email_downloader = '{email_downloader}';"""

def get_song_name(id_song):
    return f"""SELECT judul FROM KONTEN WHERE id = '{id_song}';"""