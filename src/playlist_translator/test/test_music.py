import datetime


from .. import services, parsers
from ..music import Playlist


def test_playlist_from_apple_response(apple_tracks_list):
    playlist = Playlist.from_apple_tracks_list(apple_tracks_list)
    assert playlist
    song = playlist.songs[0]
    for track in apple_tracks_list:
        track_attrs = track['attributes']
        assert song.song_id == track['id']
        assert song.service_name == 'Apple'
        assert song.name == track_attrs['name']
        assert song.artist.name == track_attrs['artistName']
        assert (song.release_date ==
                parsers.parse_apple_date(track_attrs['releaseDate']))
        assert song.album_name == track_attrs['albumName']
        assert song.track_number == track_attrs['trackNumber']
        assert song.composer_name == track_attrs['composerName']


def test_playlist_from_gplay_response(gplay_response):
    playlist = Playlist.from_gplay_response(gplay_response)
    assert playlist
    for position, orig_entry in enumerate(gplay_response):
        song = playlist.songs[position]
        orig_track = orig_entry['track']
        assert song.song_id == orig_entry['id']
        assert song.service_name == 'GPlay'
        assert song.name == orig_track['title']
        assert song.artist.name == orig_track['artist']
        assert song.release_date == datetime.date(orig_track['year'], 1, 1)
        assert song.album_name == orig_track['album']
        assert song.track_number == orig_track['trackNumber']
        assert song.composer_name == (orig_track['composer'] or None)
