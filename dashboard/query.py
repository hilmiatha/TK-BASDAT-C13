def get_user_by_email():
    return """
            SELECT * FROM AKUN
            WHERE email = %s
        """

def get_label_by_email():
    return """
        SELECT * FROM LABEL
        WHERE email = %s
    """

def get_user_playlist():
    return """
        SELECT * FROM USER_PLAYLIST
        WHERE email_pembuat = %s
    """

def get_song_by_id_artist():
    return """
        SELECT S.*, K.*
        FROM SONG S
        JOIN ARTIST A ON S.id_artist = A.id
        JOIN KONTEN K ON S.id_konten = K.id
        WHERE A.email_akun =  %s
    """

def get_song_by_songwriter():
    return """
        SELECT S.*, K.*
        FROM SONGWRITER_WRITE_SONG SWS
        JOIN SONG S ON S.id_konten = SWS.id_song
        JOIN SONGWRITER SW ON SW.id = SWS.id_songwriter
        JOIN KONTEN K ON SWS.id_song = K.id
        WHERE SW.email_akun = %s
    """

def get_podcast_by_podcaster():
    return """
        SELECT K.*
        FROM PODCAST P
        JOIN PODCASTER PO ON PO.email = P.email_podcaster
        JOIN KONTEN K ON K.id = P.id_konten
        WHERE PO.email = %s
    """

def get_album_by_id_label():
    return """
        SELECT A.*
        FROM ALBUM A
        JOIN LABEL L ON L.id = A.id_label
        WHERE L.id = %s 
    """