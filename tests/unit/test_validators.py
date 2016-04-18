from api_star import utils, validators
import datetime
import decimal
import pytest


def valid(validator, items):
    for value, expected in items:
        try:
            assert validator(value) == expected
        except validators.ValidationError as exc:  # pragma: no cover
            msg = 'Unexpected ValidationError "{error}" for value {value}.'.format(
                error=exc.description,
                value=value
            )
            raise AssertionError(msg)


def invalid(validator, items):
    for value, expected_description in items:
        with pytest.raises(validators.ValidationError) as excinfo:
            validator(value)
        exception = excinfo.value
        assert exception.description == expected_description


# Boolean validators.

def test_boolean():
    validator = validators.boolean()
    valid(validator, [
        (1, True),
        (True, True),
        ('true', True),
        (0, False),
        (False, False),
        ('false', False),
        ('', False)
    ])
    invalid(validator, [
        (None, validators.errors['null']),
        ({}, validators.errors['type'].format(type_name='boolean')),
        ('other', validators.errors['value'].format(type_name='boolean'))
    ])

    validator = validators.boolean(allow_blank=False)
    invalid(validator, [
        ('', validators.errors['blank'])
    ])


def test_nullable_boolean():
    validator = validators.nullable_boolean()
    valid(validator, [
        ('true', True),
        ('false', False),
        (None, None),
        ('', None)
    ])


# Text validators.

def test_text():
    validator = validators.text(max_length=100, min_length=3)
    valid(validator, [
        ('abc', 'abc'),
        (' abc ', 'abc'),
    ])
    invalid(validator, [
        (99, validators.errors['type'].format(type_name='string')),
        ('a' * 999, validators.errors['max_length'].format(max_length=100)),
        ('a', validators.errors['min_length'].format(min_length=3)),
        (None, validators.errors['null']),
        ('', validators.errors['blank']),
        (' ', validators.errors['blank'])
    ])

    validator = validators.text(allow_blank=True)
    valid(validator, [
        ('', ''),
        (' ', '')
    ])


def test_email():
    validator = validators.email()
    valid(validator, [
        ('user@example.com', 'user@example.com'),
        (' user@example.com ', 'user@example.com'),
    ])
    invalid(validator, [
        ('z' * 255, validators.errors['max_length'].format(max_length=254)),
        ('example.com', validators.errors['value'].format(type_name='email')),
    ])


def test_url():
    validator = validators.url()
    valid(validator, [
        ('http://example.com', 'http://example.com'),
        (' http://example.com ', 'http://example.com'),
    ])
    invalid(validator, [
        ('z' * 2001, validators.errors['max_length'].format(max_length=2000)),
        ('example.com', validators.errors['value'].format(type_name='url')),
    ])


# Numeric validators.

def test_integer():
    validator = validators.integer(min_value=100, max_value=1000)
    valid(validator, [
        ('123', 123),
        (123, 123),
        (123.1, 123)
    ])
    invalid(validator, [
        (99, validators.errors['min_value'].format(min_value=100)),
        (1001, validators.errors['max_value'].format(max_value=1000)),
        ('123abc', validators.errors['value'].format(type_name='integer')),
        ({}, validators.errors['type'].format(type_name='integer')),
        ('9' * 1000, validators.errors['too_large']),
        (None, validators.errors['null']),
        ('', validators.errors['blank'])
    ])

    validator = validators.integer(allow_null=True)
    valid(validator, [
        (None, None)
    ])


def test_number():
    validator = validators.number(min_value=100.0, max_value=1000.0)
    valid(validator, [
        ('123', 123.0),
        (123, 123.0),
        (123.1, 123.1)
    ])
    invalid(validator, [
        (99, validators.errors['min_value'].format(min_value=100.0)),
        (1001, validators.errors['max_value'].format(max_value=1000.0)),
        ('123abc', validators.errors['value'].format(type_name='number')),
        ({}, validators.errors['type'].format(type_name='number')),
        ('9' * 1000, validators.errors['too_large']),
        (None, validators.errors['null']),
        ('', validators.errors['blank'])
    ])

    validator = validators.number(allow_null=True)
    valid(validator, [
        (None, None)
    ])


def test_fixed_precision():
    validator = validators.fixed_precision(minor_digits=2, major_digits=3)
    valid(validator, [
        ('123', decimal.Decimal('123.00')),
        ('123.45', decimal.Decimal('123.45')),
        (0.12345, decimal.Decimal('0.12')),
        (12.345, decimal.Decimal('12.35'))
    ])
    invalid(validator, [
        (1000, validators.errors['max_value'].format(max_value=999.99)),
        (999.999, validators.errors['max_value'].format(max_value=999.99)),
        ('123abc', validators.errors['value'].format(type_name='number')),
        ({}, validators.errors['type'].format(type_name='number')),
        ('9' * 1000, validators.errors['too_large']),
        (None, validators.errors['null']),
        ('', validators.errors['blank'])
    ])

    validator = validators.fixed_precision(allow_null=True, min_value=10)
    valid(validator, [
        (None, None),
        ('99.99', decimal.Decimal('99.99'))
    ])
    invalid(validator, [
        (9, validators.errors['min_value'].format(min_value=10))
    ])


# Date & time validators.

def test_iso_date():
    validator = validators.iso_date()
    valid(validator, [
        (datetime.date(2001, 1, 1), datetime.date(2001, 1, 1)),
        ('2001-01-01', datetime.date(2001, 1, 1)),
    ])
    invalid(validator, [
        (datetime.datetime(2001, 1, 1, 12, 0), validators.errors['type'].format(type_name='date')),
        (2001, validators.errors['type'].format(type_name='date')),
        ('abc', validators.errors['value'].format(type_name='date')),
        ('9' * 1000, validators.errors['too_large']),
        (None, validators.errors['null']),
        ('', validators.errors['blank']),
    ])

    validator = validators.iso_date(allow_null=True)
    valid(validator, [
        ('', None),
        (None, None)
    ])


def test_iso_time():
    validator = validators.iso_time()
    valid(validator, [
        (datetime.time(12, 0), datetime.time(12, 0)),
        ('12:00', datetime.time(12, 0)),
        ('12:00:00', datetime.time(12, 0)),
        ('12:00:00.123456', datetime.time(12, 0, 0, 123456)),
    ])
    invalid(validator, [
        (datetime.date(2001, 1, 1), validators.errors['type'].format(type_name='time')),
        (2001, validators.errors['type'].format(type_name='time')),
        ('abc', validators.errors['value'].format(type_name='time')),
        ('9' * 1000, validators.errors['too_large']),
        (None, validators.errors['null']),
        ('', validators.errors['blank']),
    ])

    validator = validators.iso_time(allow_null=True)
    valid(validator, [
        ('', None),
        (None, None)
    ])


def test_iso_datetime():
    validator = validators.iso_datetime()
    valid(validator, [
        (datetime.datetime(2001, 1, 1, 12, 0), datetime.datetime(2001, 1, 1, 12, 0)),
        ('2001-01-01T12:00', datetime.datetime(2001, 1, 1, 12, 0)),
        ('2001-01-01T12:00:00', datetime.datetime(2001, 1, 1, 12, 0)),
        ('2001-01-01T12:00:00.123456', datetime.datetime(2001, 1, 1, 12, 0, 0, 123456)),
        ('2001-01-01T12:00:00Z', datetime.datetime(2001, 1, 1, 12, 0, tzinfo=utils.utc)),
        ('2001-01-01T12:00:00+00:00', datetime.datetime(2001, 1, 1, 12, 0, tzinfo=utils.utc)),
        ('2001-01-01T12:00:00-01:00', datetime.datetime(2001, 1, 1, 12, 0, tzinfo=utils.FixedOffset(-60))),
    ])
    invalid(validator, [
        (datetime.date(2001, 1, 1), validators.errors['type'].format(type_name='datetime')),
        (2001, validators.errors['type'].format(type_name='datetime')),
        ('abc', validators.errors['value'].format(type_name='datetime')),
        ('9' * 1000, validators.errors['too_large']),
        (None, validators.errors['null']),
        ('', validators.errors['blank']),
    ])

    validator = validators.iso_datetime(allow_null=True, default_timezone=utils.utc)
    valid(validator, [
        ('', None),
        (None, None),
        ('2001-01-01T12:00', datetime.datetime(2001, 1, 1, 12, 0, tzinfo=utils.utc)),
    ])


# Composite validators.

def test_list_of():
    validator = validators.list_of(validators.integer())
    valid(validator, [
        ([0, '1', 2.0], [0, 1, 2]),
        ([], [])
    ])
    invalid(validator, [
        ('foo', validators.errors['type'].format(type_name='list')),
        ([0, '1', 'abc'], validators.errors['index'].format(index=2) + ' ' + validators.errors['value'].format(type_name='integer')),
    ])

    validator = validators.list_of(validators.integer(), allow_empty=False)
    invalid(validator, [
        ([], validators.errors['empty'])
    ])


def test_mapping_of():
    validator = validators.mapping_of(validators.integer())
    valid(validator, [
        ({'a': 0, 'b': '1'}, {'a': 0, 'b': 1}),
    ])
    invalid(validator, [
        ('foo', validators.errors['type'].format(type_name='object')),
        ({'a': 0, 'b': 'abc'}, {'b': validators.errors['value'].format(type_name='integer')}),
    ])

    validator = validators.mapping_of(validators.integer(), allow_empty=False)
    invalid(validator, [
        ({}, validators.errors['empty'])
    ])


def test_object_of():
    validator = validators.object_of({
        'integer': validators.optional(validators.integer(), default=0),
        'boolean': validators.boolean()
    })
    valid(validator, [
        ({'integer': 123.0, 'boolean': 'true'}, {'integer': 123, 'boolean': True}),
        ({'integer': '123', 'boolean': True}, {'integer': 123, 'boolean': True}),
        ({'boolean': 'true'}, {'integer': 0, 'boolean': True}),
    ])
    invalid(validator, [
        ({'integer': 123.0}, {'boolean': validators.errors['required']}),
        ({'integer': 'abc', 'boolean': True}, {'integer': validators.errors['value'].format(type_name='integer')}),
        ('foo', validators.errors['type'].format(type_name='object'))
    ])
