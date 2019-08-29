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


def test_token(mocker, apple):
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

    encode = mocker.patch('jwt.encode')
    encoded_result = mocker.MagicMock()
    encode.return_value = encoded_result
    token = apple._token
    jwt.encode.assert_called_once_with(payload,
                                       secret,
                                       algorithm=alg,
                                       headers=headers)
    assert token == encoded_result.decode()
