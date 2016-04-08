from api_star.frameworks.flask import App
from api_star.renderers import CoreJSONRenderer, DocsRenderer
from api_star.validators import iso_date


app = App(__name__, title='Day of Week API')


@app.get('/', renderers=[CoreJSONRenderer(), DocsRenderer()], exclude_from_schema=True)
def root():
    return app.schema


@app.get('/day-of-week/')
def day_of_week(date):
    """
    Returns the day of the week, for the given date.
    """
    date = iso_date()(date)
    return {'day': date.strftime('%A')}
