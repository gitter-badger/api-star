from api_star.decorators import validate
from api_star.frameworks.falcon import App
from api_star.renderers import CoreJSONRenderer, DocsRenderer
from api_star.validators import iso_date


app = App(__name__, title='Day of Week API')


@app.get('/', renderers=[CoreJSONRenderer(), DocsRenderer()], exclude_from_schema=True)
def root():
    return app.schema


@app.get('/day-of-week/')
@validate(date=iso_date())
def day_of_week(date):
    """
    Returns the day of the week, for the given date.
    """
    return {'day': date.strftime('%A')}
