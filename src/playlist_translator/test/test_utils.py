import os

import pytest

from .. import utils


def test_get_environ():
    key = "key"
    var = "var"
    os.environ[key] = var
    env_var = utils.get_environ(key)
    assert env_var == var


def test_get_environ_fail():
    key = "not-an-env-var"
    with pytest.raises(OSError):
        utils.get_environ(key)
