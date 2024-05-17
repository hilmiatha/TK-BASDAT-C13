def get_charts():
    return f"""
    SELECT tipe, id_playlist FROM chart;
"""

def get_songs_chart(id_playlist):
    return f"""
    SELECT 
        K.judul AS judul_lagu, 
        AK.nama AS oleh, 
        K.tanggal_rilis AS tanggal_rilis, 
        S.total_play AS total_plays, 
        S.id_konten AS id_konten
    FROM
        playlist_song AS ps
        JOIN song AS s ON ps.id_song = s.id_konten
        JOIN konten AS k ON s.id_konten = k.id
        JOIN artist AS a ON s.id_artist = a.id
        JOIN akun AS ak ON ak.email = a.email_akun
    WHERE 
        ps.id_playlist = '{id_playlist}' 
        AND s.total_play != 0
    ORDER BY 
        s.total_play DESC
    LIMIT 20;
"""

def get_chart_info(id_playlist):
    return f""" SELECT 
 	tipe as tipe
 from 
 	CHART
 where 
 	CHART.id_playlist  = '{id_playlist}';"""