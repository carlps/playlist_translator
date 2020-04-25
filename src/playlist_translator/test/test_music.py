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


@pytest.fixture
def gplay_response():
    return [{'kind': 'sj#playlistEntry',
             'id': 'AMaBXymRY7J_cgMgbU0Sz8vdF-AI4I-6r2a8XkXhacGN6AP2vfDiJglygfA1FMbs2vrwMvFX52bbJS3EMM1h5dlzSp8I36VEmQ==',
             'absolutePosition': '01729382256910270462',
             'trackId': 'Tecwhopx5pheivs66bqszubdyhy',
             'creationTimestamp': '1555170814541380',
             'lastModifiedTimestamp': '1555170814541380',
             'deleted': False,
             'source': '2',
             'track': {'kind': 'sj#track',
                       'title': 'Public Service Announcement (interlude)',
                       'artist': 'JAY-Z',
                       'composer': '',
                       'album': 'The Black Album',
                       'albumArtist': 'JAY-Z',
                       'year': 2003,
                       'trackNumber': 10,
                       'genre': 'Hip-Hop/Rap',
                       'durationMillis': '173000',
                       'albumArtRef': [{'kind': 'sj#imageRef',
                                        'url': 'http://lh3.googleusercontent.com/_3ji08eU7E6f7cGZgzZHTS-D-UPx9Cdx1rC-8lyXULmK95AiIj-bvKOc_cwIPZQTputjO6bGn0A',
                                        'aspectRatio': '1',
                                        'autogen': False}],
                       'artistArtRef': [{'kind': 'sj#imageRef',
                                         'url': 'http://lh3.googleusercontent.com/weLyqAyDxXtO4n0f1TpwmG_TLgpAhVK0x3jFnJzWgi9Fz-qbVEoPSd54Swl8CZRe0zJ4e5uw4Q',
                                         'aspectRatio': '2',
                                         'autogen': False}],
                       'playCount': 9,
                       'discNumber': 1,
                       'estimatedSize': '6922486',
                       'trackType': '7',
                       'storeId': 'Tecwhopx5pheivs66bqszubdyhy',
                       'albumId': 'Beuxsnb2og5vxeypi25l4cz2g34',
                       'artistId': ['Axul4z6ed3pmgb5hm5gqx4fta2e'],
                       'nid': 'ecwhopx5pheivs66bqszubdyhy',
                       'trackAvailableForSubscription': True,
                       'trackAvailableForPurchase': True,
                       'albumAvailableForPurchase': False,
                       'explicitType': '1'}},
            {'kind': 'sj#playlistEntry',
             'id': 'AMaBXymRY7J_cgMgbU0Sz8vdF-AI4I-6r2a8XkXhacGN6AP2vfDiJglygfA1FMbs2vrwMvFX52bbJS3EMM1h5dlzSp8I36VEmQ==',
             'absolutePosition': '01921535841011411624',
             'trackId': 'Ttirbxrtyhopooa2wkuifltzpma',
             'creationTimestamp': '1555170881516102',
             'lastModifiedTimestamp': '1555170881516102',
             'deleted': False,
             'source': '2',
             'track': {'kind': 'sj#track',
                       'title': 'Paranoid Android',
                       'artist': 'Radiohead',
                       'composer': '',
                       'album': 'OK Computer',
                       'albumArtist': 'Radiohead',
                       'year': 1997,
                       'trackNumber': 2,
                       'genre': 'Brit Pop/Brit Rock',
                       'durationMillis': '387000',
                       'albumArtRef': [{'kind': 'sj#imageRef',
                                        'url': 'http://lh3.googleusercontent.com/FOJ-SO0djyr7GEFpkMJbiS-dtOltviBJwKF0lkR2F8cK1BY62jAVPfXnv-E_CrkOsfYxOxgb',
                                        'aspectRatio': '1',
                                        'autogen': False}],
                       'artistArtRef': [{'kind': 'sj#imageRef',
                                         'url': 'http://lh3.googleusercontent.com/53cYhGcuBl6tJh4NAsrkxHW2dYReUv27bwrA1nb_KNCrgIKeGjhfl-NmUzsu6mJGoyg1UBuvpDM',
                                         'aspectRatio': '2',
                                         'autogen': False}],
                       'playCount': 1,
                       'discNumber': 1,
                       'estimatedSize': '15491684',
                       'trackType': '7',
                       'storeId': 'Ttirbxrtyhopooa2wkuifltzpma',
                       'albumId': 'Bc5lmah5b34pzehbpiccirz3hme',
                       'artistId': ['A3qpbllyfot4yhqo7isoomtctli'],
                       'nid': 'tirbxrtyhopooa2wkuifltzpma',
                       'trackAvailableForSubscription': True,
                       'trackAvailableForPurchase': True,
                       'albumAvailableForPurchase': False,
                       'explicitType': '2'}}]

def test_playlist_from_gplay_response(gplay_response):
    playlist = Playlist.from_gplay_response(gplay_response)
    assert playlist
    assert playlist.service == services.GooglePlay
    for position, orig_entry in enumerate(gplay_response):
        song = playlist.songs[position]
        orig_track = orig_entry['track']
        assert song.service_id == orig_entry['trackId']
        assert song.name == orig_track['title']
        assert song.artist.name == orig_track['artist']
        assert song.url is None
        assert song.release_date == datetime.date(orig_track['year'], 1, 1)
        assert song.album_name == orig_track['album']
        assert song.track_number == orig_track['trackNumber']
        assert song.composer_name == orig_track['composer']