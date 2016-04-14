# Validators

API star provides a number of validators that allow you to clean and verify
the incoming data to your API. For example, if you have an input that should
be a valid date string, you can use the `iso_date()` validator to verify the
input.

    @app.get('/day-of-week/')
    @validate(date=iso_date())
    def day_of_week(date):
        return {'day': date.isoformat('%A')}

When validation fails on a view a 400 response will be returned, including an
error message describing the input that failed.

    GET 127.0.0.1:5000/day-of-week/?date=2001-01-99

    HTTP/1.1 400 Bad Request
    {
        "date": "Not a valid date value."
    }

## Using validators

A validator is a *callable* that takes a single value, and returns some validated data.

    >>> from api_star import validators
    >>> validator = validators.integer()
    >>> validator('123')
    123

Validators should raise a `ValidationError` if validation fails.

    >>> validator('abc')
    Traceback:
        ...
    api_star.exceptions.ValidationError: 'Not a valid integer value.'

Some validators may include parameters.

    >>> validator = validators.text(max_length=10)
    >>> validator('abcdefghijklmnopqrstuvwxyz')
    Traceback:
        ...
    api_star.exceptions.ValidationError: 'Length must not be greater than 10.'

You can apply validators to the arguments of any function, using the
`@validate` decorator.

    >>> @validate(
    ...     date_from=validators.iso_date(),
    ...     date_to=validators.iso_date()
    ... )
    ... def duration(date_from, date_to):
    ...    return (date_to - date_from).days
    ...
    >>> duration("2001-01-01", "2002-01-01")
    365
    >>> duration("2001-01-01", "2002-01-99")
    Traceback (most recent call last):
        ...
    api_star.exceptions.ValidationError: {'date_to': 'Not a valid date value.'}

If you need to apply a constraint across more than one input, you should do so
by raising a `ValidationError` inside the function.

    >>> @validate(
    ...     date_from=validators.iso_date(),
    ...     date_to=validators.iso_date()
    ... )
    ... def duration(date_from, date_to):
    ...     if date_to < date_from:
    ...         raise exceptions.ValidationError('`date_to` must not be earlier than `date_from`.')
    >>>     return (date_to - date_from).days

## Custom validators

### Using a plain function

The simplest way to create a validator is to write it as a function.

    def hex_color(value):
        """
        Validates a hexadecimal color representation, such as "#FFD700".
        Returns the result as a three-tuple of integers, such as (255, 215, 0).
        """
        try:
            match = re.match('#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})', value)
        except TypeError:
            raise ValidationError('Must be a string.')
        if not match:
            raise ValidationError('Not a valid hex color.')

        return tuple([int(hex_string, 16) for hex_string in match.groups()])

### Using a parameterized function

You can also provide a parameterized validator, by using a function that
takes the required parameters and returns the validator function.

    def hex_color(allow_null=False):
        regex = re.compile('#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})')

        def validator(value):
            if value in ('', None):
                if allow_null:
                    return None
                raise ValidationError('May not be null')

            try:
                match = regex.match(value)
            except TypeError:
                raise ValidationError('Must be a string')
            if not match:
                raise ValidationError('Not a valid hex color.')

            return tuple([int(hex_string, 16) for hex_string in match.groups()])

        return validator

To use this validator it must first be instantiated. In this case either
`hex_color()`, or `hex_color(allow_null=True)`.
