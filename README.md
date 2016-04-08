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

    app = App(__name__, title='Day of week API')

    @app.get('/day-of-week/')
    def day_of_week(date):
        """
        Returns the day of the week for the given date.
        """
        date = iso_date()(date)
        return {'day': date.strftime('%A')}

Now let's run the service:

    $ flask --app=example_api run

Now we can interact with the API

    $ curl http://127.0.0.1:5000/day-of-week/?date=1979-03-04
    {"day": "Sunday"}

## Schema generation & client libraries.

API Star provides automatic schema generation, and can render the schema into various formats.

Once you've included a schema, clients can inspect and interact with your API using the `coreapi` dynamic client library.

    $ pip install coreapi
    $ coreapi get http://127.0.0.1:5000/
    <Day of week API "http://127.0.0.1:5000/">
        day_of_week(date)
    $ coreapi action day_of_week --param date 1979-03-04
    {"day": "Sunday"}

## Documentation

More complete project documentation is available at http://api-star.com/

* [Frameworks](http://api-star.com/frameworks/)
* [Parsers](http://api-star.com/parsers/)
* [Renderers](http://api-star.com/renderers/)
* [Authentication](http://api-star.com/authentication/)
* [Permissions](http://api-star.com/permissions/)
* [Validation](http://api-star.com/validation/)
* [Schemas](http://api-star.com/schemas/)
* [Client library](http://api-star.com/client-library/)
