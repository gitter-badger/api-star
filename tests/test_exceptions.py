from api_star.exceptions import APIException


def test_custom_exception():
    exc = APIException('Something failed', 418)
    assert exc.code == 418
    assert 'error: %s' % exc == 'error: Something failed'
