# API Star

[![Join the chat at https://gitter.im/tomchristie/api-star](https://badges.gitter.im/tomchristie/api-star.svg)](https://gitter.im/tomchristie/api-star?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![travis-badge]][travis]
[![pypi-badge]][pypi]

*An API framework for Flask & Falcon.*

* Flask and Falcon backends.
* Automatic schema & documentation generation.
* Dynamic client libraries for interacting with your APIs.

## Requirements

Python 2.7 or 3.4+.

## Getting started

For this example we'll use Flask.

    $ pip install api-star
    $ pip install flask flask-cli

Here's our first API, which takes a date as a string like "2000-01-01", and returns the day of the week, such as "Saturday". Put this in a file named `example.py`:

    from api_star.decorators import validate
    from api_star.frameworks.flask import App
    from api_star.validators import iso_date

    app = App(__name__, title='Day of Week API')

    @app.get('/day-of-week/')
    @validate(date=iso_date())
    def day_of_week(date):
        """
        Returns the day of the week, for the given date.
        """
        return {'day': date.strftime('%A')}

Now let's run the service:

    $ flask --app=example --debug run

Now we can interact with the API

    $ curl http://127.0.0.1:5000/day-of-week/?date=1979-03-04
    {"day": "Sunday"}

## Alternative backends

We can also switch over to using the Falcon backend.
First we'll edit the `App` import line.

    from api_star.frameworks.falcon import App

Now install Falcon and the gunicorn WSGI server, and start the API again:

    $ pip install falcon gunicorn
    $ gunicorn -b localhost:5000 example:app

## Documentation & schema generation

API Star provides support for automatic documentation and schema generation.
Let's add an endpoint that will render API documentation to support this.

    from api_star.renderers import corejson_renderer, docs_renderer

    @app.get('/', renderers=[corejson_renderer(), docs_renderer()], exclude_from_schema=True)
    def root():
        return app.schema

Now when we visit the endpoint in a browser we get some API documentation.

![Documentation screenshot](https://raw.githubusercontent.com/tomchristie/api-star/master/docs/screenshot.png)

Or if we request the endpoint with a command-line client, we get a schema.

    $ curl http://127.0.0.1:5000/
    {"_type":"document","_meta":{"title":"Day of Week API"},"day_of_week":{"_type":"link","url":"/day-of-week/","action":"GET","description":"Returns the day of the week, for the given date.","fields":[{"name":"date","required":true,"location":"query"}]}}

## Client libraries

Once you've included a schema, clients can inspect and interact with your
deployed API using the `coreapi` command-line client.

    $ pip install coreapi
    $ coreapi get http://127.0.0.1:5000/
    <Day of Week API "http://127.0.0.1:5000/">
        day_of_week(date)
    $ coreapi action day_of_week --param date 1979-03-04
    {"day": "Sunday"}

## Testing

Call API functions directly:

    assert day_of_week(date='2000-01-01') == {'day': 'Saturday'}

Use `TestSession` to call into your API using the `requests` library:

    from api_star.test import TestSession
    from my_project import app

    session = TestSession(app)
    response = session.get('/day-of-week/', params={'date': '2000-01-01'})
    assert response.status_code == 200
    assert response.json() == {'day': 'Saturday'}

## Configuration

Use `Environment` to configure your application based on environment variables:

    from api_star import validators
    from api_star.environment import Environment

    env = Environment(
        DEBUG=(validators.boolean(), "True"),
        SECRET_KEY=(validators.string(), "290f6f17c13945aa")
    )

    env.DEBUG  # Defaults to `True`, unless environment variable is set.

[travis-badge]: https://travis-ci.org/tomchristie/api-star.svg?branch=master
[travis]: https://travis-ci.org/tomchristie/api-star
[pypi-badge]: https://img.shields.io/pypi/v/api-star.svg
[pypi]: https://pypi.python.org/pypi/api-star
