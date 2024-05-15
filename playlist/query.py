
from uuid import uuid4


def get_playlist(email_pembuat):
    return f"""SELECT * FROM user_playlist WHERE email_pembuat = '{email_pembuat}';"""


def get_playlist_detail(id_playlist):
    return f"""SELECT 
  k.judul AS judul_lagu, 
  ak.nama AS oleh, 
  k.durasi AS durasi,
  k.id as id_lagu
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

def get_playlist_info(id_playlist):
    return f""" select 
 	*
 from 
 	user_playlist
 where 
 	user_playlist.id_playlist  = '{id_playlist}';"""
  
def get_lagu():
  return f""" select 
 	k.id as id_lagu, 
 	k.judul as judul_lagu,
 	ak.nama as nama_penyanyi
 from
 	konten as k,
 	song as s,
 	artist as a,
 	akun as ak
 where s.id_konten = k.id and s.id_artist = a.id and ak.email = a.email_akun;"""
 
 
def get_judul_deskripsi_playlist(id_playlist):
    return f"""select judul, deskripsi from user_playlist where id_playlist = '{id_playlist}';"""


def insert_playlist(email_pembuat, judul, deskripsi):
    uuid_playlist = str(uuid4())
    uuid_user_playlist = str(uuid4())
    return f"""INSERT INTO playlist (id)
VALUES ('{uuid_playlist}');
INSERT INTO user_playlist (email_pembuat, id_user_playlist, judul, deskripsi, jumlah_lagu, tanggal_dibuat, id_playlist, total_durasi)
VALUES ('{email_pembuat}', '{uuid_user_playlist}', '{judul}', '{deskripsi}', 0, current_date, '{uuid_playlist}', 0);"""


def delete_playlist(id_user_playlist, id_playlist):
    return f"""DELETE FROM playlist WHERE id = '{id_playlist}';
DELETE FROM user_playlist
WHERE id_user_playlist = '{id_user_playlist}';
DELETE FROM playlist_song
WHERE id_playlist = '{id_playlist}';
DELETE FROM akun_play_user_playlist
WHERE id_user_playlist = '{id_user_playlist}';"""

def update_playlist(title, description, id_user_playlist):
    return f"""UPDATE user_playlist
SET judul = '{title}', deskripsi = '{description}'
WHERE id_user_playlist = '{id_user_playlist}';"""

def insert_playlist_song(id_playlist, id_lagu, durasi):
    return f"""INSERT INTO playlist_song (id_playlist, id_song)
VALUES ('{id_playlist}', '{id_lagu}');
UPDATE user_playlist
SET jumlah_lagu = jumlah_lagu + 1, total_durasi = total_durasi + {durasi}
WHERE id_playlist = '{id_playlist}';"""
  
  
  
  
  
  
#============================================= FITUR 2 ============================================

def get_atribut_lagu_except_songwriter(id_song):
    return f"""select
	k.judul as judul_lagu,
	string_agg(g.genre, ',') as genre,
	ak.nama as nama_penyanyi,
	k.durasi,
	k.tanggal_rilis,
	k.tahun,
	s.total_play,
	s.total_download,
	ab.judul,
  s.id_konten
from
	konten k, genre g, akun ak, songwriter_write_song sws, songwriter sw, song s, album ab, artist ar
where 
	s.id_konten = '{id_song}' and 
	s.id_konten = k.id and
	s.id_konten = g.id_konten and 
	s.id_artist = ar.id and 
	ar.email_akun = ak.email and
	sws.id_song = s.id_konten and 
	sw.id = sws.id_songwriter and 
	ab.id = s.id_album 
group by judul_lagu, nama_penyanyi,k.durasi,
	k.tanggal_rilis,
	k.tahun,
	s.total_play,
	s.total_download,
	ab.judul, s.id_konten ;"""
 
def get_songwriter_from_song(id_song):
    return f"""select 
	string_agg(akun.nama, ',') as songwriter, song.id_konten 
from
	song, songwriter_write_song, akun, songwriter
where 
	song.id_konten = '{id_song}' and 
	song.id_konten = songwriter_write_song.id_song and 
	songwriter_write_song.id_songwriter = songwriter.id and 
	songwriter.email_akun = akun.email 
group by song.id_konten;"""

def get_playlist_per_user(email):
    return f"""SELECT * FROM user_playlist WHERE email_pembuat = '{email}';"""