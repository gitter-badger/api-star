# API Star

*An API framework for either Flask or Falcon.*

* Support for Python 2.7 or 3.4+.
* Flask and Falcon backends.
* Automatic schema & documentation generation.
* Dynamic client libraries for interacting with your APIs.

## Getting started.

For this example we'll use Flask.

    $ pip install api-star
    $ pip install flask flask-cli

Here's our first API, which takes a date as a string like "2000-01-01", and returns the day of the week, such as "Saturday". Put this in a file named `example_api.py`:

    from api_star.frameworks.flask import App
    from api_star.validators import iso_date

    app = App(__name__, title='Day of Week API')

    @app.get('/day-of-week/')
    def day_of_week(date):
        """
        Returns the day of the week for the given date.
        """
        date = iso_date()(date)
        return {'day': date.strftime('%A')}

Now let's run the service:

    $ flask --app=example_api --debug run

Now we can interact with the API

    $ curl http://127.0.0.1:5000/day-of-week/?date=1979-03-04
    {"day": "Sunday"}

## Documentation, schema generation & client libraries.

API Star provides support for automatic documentation and schema generation.
Let's add an endpoint that will render API documentation when requested
by a browser, or a schema when requested by an API client.

    from api_star import renderers

    @app.get('/', renderers=[CoreJSONRenderer(), DocsRenderer()], exclude_from_schema=True)
    def root():
        return app.schema

Once you've included a schema, clients can inspect and interact with your
deployed API using the `coreapi` dynamic client library.

    $ pip install coreapi
    $ coreapi get http://127.0.0.1:5000/
    <Day of Week API "http://127.0.0.1:5000/">
        day_of_week(date)
    $ coreapi action day_of_week --param date 1979-03-04
    {"day": "Sunday"}
