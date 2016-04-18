from api_star.environment import Environment
from api_star import validators
import os


def test_default():
    env = Environment(
        EXAMPLE=(validators.integer(), '123')
    )
    assert env.EXAMPLE == 123


def test_set_variable():
    os.environ['EXAMPLE'] = '456'
    env = Environment(
        EXAMPLE=(validators.integer(), '123')
    )
    assert env.EXAMPLE == 456
