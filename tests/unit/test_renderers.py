from api_star.renderers import (
    json_renderer, corejson_renderer, docs_renderer, html_renderer
)
import coreapi


def test_json_renderer():
    renderer = json_renderer()
    assert renderer({'hello': 'world'}) == b'{"hello":"world"}'

    renderer = json_renderer(verbose=True)
    assert renderer({'hello': 'world'}) == b'{\n    "hello": "world"\n}'

    renderer = json_renderer()
    assert (
        renderer({'unicode snowman': u'\u2603'}) ==
        b'{"unicode snowman":"' + u'\u2603'.encode('utf-8') + b'"}'
    )


def test_corejson_renderer():
    doc = coreapi.Document(title='Example', content={'hello': 'world'})

    renderer = corejson_renderer()
    assert renderer(doc) == b'{"_type":"document","_meta":{"title":"Example"},"hello":"world"}'

    renderer = corejson_renderer(verbose=True)
    assert renderer(doc) == b'{\n    "_type": "document",\n    "_meta": {\n        "title": "Example"\n    },\n    "hello": "world"\n}'


def test_docs_renderer():
    doc = coreapi.Document(title='Example', content={'hello': 'world'})

    renderer = docs_renderer()
    assert '<title>Example</title>' in renderer(doc)


def test_html_renderer():
    renderer = html_renderer()
    assert renderer('Hello, world.') == 'Hello, world.'
