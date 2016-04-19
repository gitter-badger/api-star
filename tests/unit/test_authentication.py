from api_star.authentication import basic_auth, token_auth
from api_star.exceptions import Unauthorized
import base64
import pytest


class MockRequest(object):
    def __init__(self, auth_header=None):
        self.headers = {}
        if auth_header:
            self.headers['Authorization'] = auth_header


def test_basic_auth():
    def lookup_username(username, password):
        if username == 'admin' and password == 'password':
            return 'admin'

    auth = basic_auth(lookup_username)

    assert auth(MockRequest()) is None
    assert auth(MockRequest(b'Token auth')) is None

    with pytest.raises(Unauthorized):
        auth(MockRequest(b'Basic'))
    with pytest.raises(Unauthorized):
        auth(MockRequest(b'Basic too many tokens'))
    with pytest.raises(Unauthorized):
        auth(MockRequest(b'Basic notbase64'))
    with pytest.raises(Unauthorized):
        auth(MockRequest(b'Basic ' + base64.b64encode(b'username_only')))
    with pytest.raises(Unauthorized):
        auth(MockRequest(b'Basic ' + base64.b64encode(b'invalid:credentials')))

    assert auth(MockRequest(b'Basic ' + base64.b64encode(b'admin:password'))) == 'admin'


def test_token_auth():
    def lookup_token(token):
        if token == 'token':
            return 'admin'

    auth = token_auth(lookup_token)

    assert auth(MockRequest()) is None
    assert auth(MockRequest(b'Basic auth')) is None

    with pytest.raises(Unauthorized):
        auth(MockRequest(b'Token'))
    with pytest.raises(Unauthorized):
        auth(MockRequest(b'Token too many tokens'))
    with pytest.raises(Unauthorized):
        auth(MockRequest(b'Token invalid'))

    assert auth(MockRequest(b'Token token')) == 'admin'
