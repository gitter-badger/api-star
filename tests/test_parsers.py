from api_star.exceptions import BadRequest
from api_star.parsers import json_parser, urlencoded_parser
from werkzeug import MultiDict
import io
import pytest


def test_json_parser():
    parser = json_parser()
    stream = io.BytesIO(b'{"hello":"world"}')
    assert parser(stream) == {"hello": "world"}

    stream = io.BytesIO(b'hello, world.')
    with pytest.raises(BadRequest):
        parser(stream)


def test_urlencoded_parser():
    parser = urlencoded_parser()
    stream = io.BytesIO(b'foo=1&bar=2')
    assert parser(stream) == MultiDict({"foo": "1", "bar": "2"})

    parser = urlencoded_parser()
    stream = io.BytesIO(b'foo=1&foo=2')
    assert parser(stream) == MultiDict([("foo", "1"), ("foo", "2")])
