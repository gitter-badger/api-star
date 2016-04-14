from api_star.permissions import is_authenticated, is_authenticated_or_read_only


class MockRequest(object):
    def __init__(self, method, auth):
        self.method = method
        self.auth = auth


def test_is_authenticated():
    perm = is_authenticated()
    assert perm(MockRequest('GET', None)) is False
    assert perm(MockRequest('GET', 'admin')) is True


def test_is_authenticated_or_read_only():
    perm = is_authenticated_or_read_only()
    assert perm(MockRequest('GET', None)) is True
    assert perm(MockRequest('GET', 'admin')) is True
    assert perm(MockRequest('POST', None)) is False
    assert perm(MockRequest('GET', 'admin')) is True
