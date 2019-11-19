import datetime

import pytest

from .. import services
from ..music import Playlist


# TODO use better test data factory
@pytest.fixture
def tracks():
    tracks = {
        'data':
        [{'id': '1234',
          'type': 'songs',
          'href': '/v1/catalog/us/songs/1234',
          'attributes':
                {'previews': [{'url': 'https://'}],
                 'artwork': {},
                 'artistName': 'The Artist',
                 'url': 'https://...',
                 'discNumber': 1,
                 'genreNames': ['Pop', 'Music'],
                 'durationInMillis': 12345,
                 'releaseDate': '2019-09-19',
                 'name': 'Song Name',
                 'isrc': 'USAM123',
                 'albumName': 'Album Name',
                 'playParams': {'id': '1234', 'kind': 'song'},
                 'trackNumber': 8,
                 'composerName': 'This Guy, That Gal',
                 },
          },
         ]
    }
    return tracks


@pytest.fixture
def apple_response(tracks):
    response = {
        'data': [
            {'id': 'pl.acc123',
             'type': 'playlist',
             'href': '/v1/catalog/us/playlists/pl.acc123',
             'attributes':
                {'artwork': {'width': 1000, 'height': 1000},
                 'isChart': False,
                 'url': 'https://app.music.com',
                 'lastModifiedDate': '2019-09-19T12:00:00Z',
                 'name': 'Great Playlist',
                 'playlistType': 'user-shared',
                 'curatorName': 'The Curator',
                 'playParams': {'id': 'pl.acc123', 'kind': 'playlist'},
                 'description': {'standard': 'A longer description',
                                 'short': 'A shorter one'},
                 },
             'relationships':
                 {'curator': {'data':
                              [{'id': '123',
                                'type': 'apple-curators',
                                'href': '/v1/...'}],
                              'href': '/v1/catalog/..'},
                  'tracks': tracks,
                  }
             }
        ]
    }
    return response


def test_playlist_from_apple_response(tracks, apple_response):
    playlist = Playlist.from_apple_response(apple_response)
    assert playlist
    assert playlist.service == services.Apple
    song = playlist.songs[0]
    for track in tracks['data']:
        track_attrs = track['attributes']
        assert song.service_id == track['id']
        assert song.name == track_attrs['name']
        assert song.artist.name == track_attrs['artistName']
        assert song.url == track_attrs['url']
        assert song.release_date == datetime.datetime.strptime(
                track_attrs['releaseDate'], services.Apple.dt_format).date()
        assert song.album_name == track_attrs['albumName']
        assert song.track_number == track_attrs['trackNumber']
        assert song.composer_name == track_attrs['composerName']
