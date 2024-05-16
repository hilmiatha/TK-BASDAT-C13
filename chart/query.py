def get_charts():
    return f"""
    SELECT tipe, id_playlist FROM chart;
"""

def get_songs_chart(id_playlist):
    return f"""
    SELECT K.judul AS judul_lagu, AK.nama AS oleh, K.tanggal_rilis AS tanggal_rilis ,S.total_play AS total_plays, S.id_konten AS id_konten
    FROM
     playlist_song AS ps, 
    song AS s, 
    konten AS k, 
    artist AS a, 
    akun AS ak
    WHERE 
    ps.id_playlist = '{id_playlist}' 
    AND ps.id_song = s.id_konten 
    AND s.id_konten = k.id
    AND s.id_artist = a.id 
    AND ak.email = a.email_akun;   
"""

def get_chart_info(id_playlist):
    return f""" SELECT 
 	tipe as tipe
 from 
 	CHART
 where 
 	CHART.id_playlist  = '{id_playlist}';"""