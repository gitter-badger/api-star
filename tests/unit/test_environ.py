from api_star.environment import Environment
from api_star import validators


def test_default():
    env = Environment(
        EXAMPLE=(validators.integer(), '123')
    )
    assert env.EXAMPLE == 123


def test_set_variable():
    class MockEnvironment(Environment):
        environ = {'EXAMPLE': '456'}

    env = MockEnvironment(
        EXAMPLE=(validators.integer(), '123')
    )
    assert env.EXAMPLE == 456
