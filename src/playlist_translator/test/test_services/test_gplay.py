import datetime

import pytest

from ...services import GPlay

@pytest.fixture
def gplay(gplay_response, monkeypatch):
    def get_playlist_response(self, playlist_id):
        return gplay_response

    monkeypatch.setattr(GPlay, 'get_playlist_response', get_playlist_response)
    # TODO - handle auth in testing

    return GPlay()


def test_playlist_from_gplay_response(gplay, gplay_response):
    playlist = gplay.get_playlist('fake_id')
    assert playlist
    for position, orig_entry in enumerate(gplay_response):
        song = playlist.songs[position]
        orig_track = orig_entry['track']
        assert song.song_id == orig_entry['id']
        assert song.name == orig_track['title']
        assert song.artist.name == orig_track['artist']
        assert song.release_date == datetime.date(orig_track['year'], 1, 1)
        assert song.album_name == orig_track['album']
        assert song.track_number == orig_track['trackNumber']
        assert song.composer_name == (orig_track['composer'] or None)
