"""
Define music services in here. All should inherit from Service.
"""
from dataclasses import dataclass
import datetime
import os
from typing import Dict, List, Optional, Tuple
from urllib import parse

from glom import glom
from gmusicapi import Mobileclient
import jwt
import requests

from .utils import get_environ
from .music import Playlist, Song


@dataclass
class Service:
    """
    """
    name: str

    @property
    def is_authenticated(self):
        raise NotImplementedError

    def get_playlist(self, playlist_id: str) -> Playlist:
        raise NotImplementedError

    def lookup_song(self, song: Song) -> Tuple[Optional[Song], Optional[str]]:
        """
        Given a Song, return this services definition of that Song
        """
        raise NotImplementedError


@dataclass
class Apple(Service):
    """
    """
    name: str = "Apple"
    base_url: str = "https://api.music.apple.com/v1/catalog/"

    tracks_glom = ('data', ['relationships.tracks.data'])
    search_songs_glom = 'results.songs.data'

    @property
    def is_authenticated(self):
        # TODO handle authentication for apple user
        return True

    @property
    def storefront(self):
        # TODO this should be set from the user
        return 'us'

    @property
    def _token(self):
        """
        JWT token needed for every call to apple music API.
        """
        # TODO - in cli present prompt for setting env if not exist
        secret = get_environ('APPLE_SECRET')

        encoded_jwt = jwt.encode(self._jwt_payload,
                                 secret,
                                 algorithm=self._jwt_headers['alg'],
                                 headers=self._jwt_headers)
        token = encoded_jwt.decode()
        return token

    @property
    def _jwt_headers(self):
        alg = get_environ('APPLE_ALG')
        key_id = get_environ('APPLE_KEY_ID')

        jwt_headers = {
            'alg': alg,
            'kid': key_id,
        }
        return jwt_headers

    @property
    def _jwt_payload(self):
        team_id = get_environ('APPLE_TEAM_ID')
        now = datetime.datetime.now()
        issued_at = int(now.timestamp())
        # TODO set expiration better
        expires_at = int((now + datetime.timedelta(hours=24)).timestamp())

        jwt_payload = {
            'iss': team_id,
            'iat': issued_at,
            'exp': expires_at,
        }
        return jwt_payload

    def _get_environ(self, var_name):
        """
        Lookup an environment variable and return it's value. Raise an error
        if it doesn't exist.
        """
        var = os.environ.get(var_name)
        if var is None:
            # TODO maybe present prompt for setting?
            # that should prob be in the cli
            msg = 'Missing required environment variable {}'.format(var_name)
            raise OSError(msg)
        return var

    @property
    def _headers(self):
        """
        Authentication headers needed for every call to apple music api.
        """
        headers = {'Authorization': 'Bearer {}'.format(self._token),
                   'Content-Type': 'application/json',
                   }
        return headers

    def get(self, url, params=None):
        response = requests.get(url, headers=self._headers, params=params)
        return response
    
    def get_playlist_response(self, playlist_id: str) -> Dict:
        url = f'{self.base_url}{self.storefront}/playlists/{playlist_id}'
        # TODO - handle bad response
        response = self.get(url)
        return response.json()

    def get_playlist(self, playlist_id: str) -> Playlist:
        response = self.get_playlist_response(playlist_id)
        tracks_list = glom(response, self.tracks_glom)
        # returns list of list. why?
        assert len(tracks_list) == 1
        return Playlist.from_apple_tracks_list(tracks_list[0])

    def _search_song(self, song: Song) -> requests.models.Response:
        # ex: search?term=james+brown&limit=2&types=artists,albums
        search_term = song.artist_track
        types = 'songs'
        params = {'term': search_term, 'types': types}
        lookup_url = f'{self.base_url}{self.storefront}/search?'
        response = self.get(lookup_url, params=params)
        return response

    def lookup_song(self, song: Song) -> Tuple[Optional[Song], Optional[str]]:
        search_results_response = self._search_song(song)
        # TODO hangle bad response
        search_results = search_results_response.json()
        songs = glom(search_results, self.search_songs_glom)
        # for now just take first result
        first_result = songs[0]
        result_song = Song.from_apple_track(first_result)
        # TODO - return error if error
        return result_song, None


@dataclass
class GPlay(Service):
    name: str = "GPlay"
    client: Mobileclient = Mobileclient()

    @property
    def is_authenticated(self):
        return self.client.is_authenticated()

    def authenticate(self):
        # TODO prob just do this on startup
        if self.is_authenticated:
            return
        if not os.path.exists(self.client.OAUTH_FILEPATH):
            # need to handle higher up i think
            self.client.perform_oauth()
        login_success = self.client.oauth_login(self.client.FROM_MAC_ADDRESS)
        if not login_success:
            # TODO better exception
            raise Exception("Could not login to {self.name}")

    def logout(self):
        self.client.logout()

    def get_playlist_response(self, playlist_id: str) -> List:
        if not self.is_authenticated:
            # TODO better exception or even better don't let this happen
            raise Exception("Must authenticate before use")
        parsed_playlist_id = parse.unquote(playlist_id)
        # TODO - handle bad response
        response = self.client.get_shared_playlist_contents(parsed_playlist_id)
        return response

    def get_playlist(self, playlist_id: str) -> Playlist:
        response = self.get_playlist_response(playlist_id)
        playlist = Playlist.from_gplay_response(response)
        return playlist

    def _search_song(self, song: Song) -> List[Dict]:
        query = song.artist_track
        search_results = self.client.search(query)
        return search_results['song_hits']

    def lookup_song(self, song: Song) -> Tuple[Optional[Song], Optional[str]]:
        results = self._search_song(song)
        # TODO handle bad response
        # for now just take first result
        result_song = Song.from_gplay_entry(results[0])
        return result_song, None


class NotAuthenticatedError(Exception):
    pass
