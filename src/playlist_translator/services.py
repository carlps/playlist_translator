"""
Define music services in here. All should inherit from Service.
"""
from dataclasses import dataclass
import datetime
import os

import jwt
import requests


@dataclass
class Service:
    """
    """
    name: str
    base_url: str

    @property
    def creds(self):
        """
        """
        raise NotImplementedError


@dataclass
class Apple(Service):
    """
    """
    name: str = "Apple"
    base_url: str = "https://api.music.apple.com/v1/catalog/"

    @property
    def storefront(self):
        # TODO this should be set from the user
        return 'us'

    @property
    def _token(self):
        """
        JWT token needed for every call to apple music API.
        """
        alg = self._get_environ('APPLE_ALG')
        key_id = self._get_environ('APPLE_KEY_ID')
        team_id = self._get_environ('APPLE_TEAM_ID')
        secret = self._get_environ('APPLE_SECRET')

        now = datetime.datetime.now()
        issued_at = int(now.timestamp())
        # TODO set expiration better
        expires_at = int((now + datetime.timedelta(hours=24)).timestamp())

        jwt_headers = {
            'alg': alg,
            'kid': key_id,
        }

        jwt_payload = {
            'iss': team_id,
            'iat': issued_at,
            'exp': expires_at,
        }

        encoded_jwt = jwt.encode(jwt_payload,
                                 secret,
                                 algorithm=alg,
                                 headers=jwt_headers)
        token = encoded_jwt.decode()
        return token

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

    def get(self, url):
        response = requests.get(url, headers=self._headers)
        return response

    def get_playlist(self, playlist_id):
        url = f'{self.base_url}{self.storefront}/playlists/{playlist_id}'
        response = self.get(url)
        return response.json()


@dataclass
class GooglePlay(Service):
    name: str = "Google Play"
    base_url: str = "TODO"
