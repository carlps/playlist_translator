import datetime
import os

import jwt
import pytest


@pytest.fixture
def apple():
    from ...services import Apple
    return Apple()


def test_name(apple):
    assert apple.name == 'Apple'


def test_storefront(apple):
    assert apple.storefront == 'us'


def test_jwt_headers(apple):
    alg = 'alg'
    key = 'key'
    os.environ['APPLE_ALG'] = alg
    os.environ['APPLE_KEY_ID'] = key
    headers = {'alg': alg, 'kid': key}
    assert apple._jwt_headers == headers


def test_jwt_payload(apple):
    team_id = 'team_id'
    os.environ['APPLE_TEAM_ID'] = team_id
    now = datetime.datetime.now()
    timestamp = int(now.timestamp())
    expires = int((now + datetime.timedelta(hours=24)).timestamp())
    payload = {'iss': team_id, 'iat': timestamp, 'exp': expires}
    # note that if this is realllly slow, the timestamps can be off, causing
    # tests to fail. should probably have better tests.
    assert apple._jwt_payload == payload


class MockToken:
    def encode(self, payload, secret, algorithm, headers):
        self.payload = payload
        self.secret = secret
        self.algorithm = algorithm
        self.headers = headers
        return self

    def decode(self):
        return self


@pytest.fixture
def mock_token(monkeypatch):
    """
    jwt token mocked to just test args and calling
    return mock token obj to ensure it's returned when decoded
    """
    token = MockToken()
    def mock_encode(*args, **kwargs):
        return token.encode(*args, **kwargs)
    monkeypatch.setattr(jwt, 'encode', mock_encode)
    return token



def test_token(mock_token, apple):
    """
    using MockToken class to ensure we are correctly calling jwt.encode and
    decode
    """
    alg = 'alg'
    key = 'key'
    team_id = 'team_id'
    secret = 'secret'
    os.environ['APPLE_ALG'] = alg
    os.environ['APPLE_KEY_ID'] = key
    os.environ['APPLE_TEAM_ID'] = team_id
    os.environ['APPLE_SECRET'] = secret

    headers = {'alg': alg, 'kid': key}

    now = datetime.datetime.now()
    timestamp = int(now.timestamp())
    expires = int((now + datetime.timedelta(hours=24)).timestamp())
    # note that if this is realllly slow, the timestamps can be off, causing
    # tests to fail. should probably have better tests.
    payload = {'iss': team_id, 'iat': timestamp, 'exp': expires}

    token = apple._token

    assert token.payload == payload
    assert token.secret == secret
    assert token.algorithm == alg
    assert token.headers == headers

    assert token == mock_token
