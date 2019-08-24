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
    name: str
    base_url: str

    @property
    def creds(self):
        raise NotImplementedError


@dataclass
class Apple(Service):
    name: str = "Apple"
    base_url: str = "TODO"

    @property
    def token(self):
        """
        Apple music suports JWT, so we can use that for credentials.
        """
        # TODO - handle missing creds
        alg = os.environ.get('APPLE_ALG')
        key_id = os.environ.get('APPLE_KEY_ID')
        team_id = os.environ.get('APPLE_TEAM_ID')
        secret = os.environ.get('APPLE_SECRET')

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

    @property
    def headers(self):
        headers = {'Authorization': 'Bearer {}'.format(self.token),
                   'Content-Type': 'application/json',
                   }
        return headers

    def get(self, url):
        response = requests.get(url, headers=self.headers)
        return response


@dataclass
class GooglePlay(Service):
    name: str = "Google Play"
    base_url: str = "TODO"
