def get_downloaded_songs(email):
    return f"""SELECT K.judul, A.nama FROM DOWNLOADED_SONG DS, SONG S, ARTIST AR, KONTEN K, AKUN A 
    WHERE DS.email_downloader = '{email}'
    and DS.id_song = S.id_konten 
    and S.id_konten = K.id 
    AND S.id_artist = AR.id 
    and AR.email_akun = A.email;"""