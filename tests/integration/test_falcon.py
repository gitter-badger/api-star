from api_star import validators
from api_star.decorators import validate
from api_star.frameworks.falcon import App
from api_star.test import TestSession


app = App(__name__, title='Day of Week API')


@app.get('/day-of-week/')
@validate(date=validators.iso_date())
def day_of_week(date):
    """
    Returns the day of the week, for the given date.
    """
    return {'day': date.strftime('%A')}


def test_success():
    session = TestSession(app)
    session.get('/day-of-week/', params={'date': '2001-01-01'})
