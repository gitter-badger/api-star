from api_star.compat import copy_signature, getargspec
from api_star.exceptions import ValidationError
from functools import wraps
import inspect


def validate(**validated):
    """
    The `validate()` function takes keyword arguments, and returns a decorator.
    """
    def decorator(func):
        """
        The decorator is called on the function that `@validate()` has been applied too.
        """
        arg_names = getargspec(func).args

        for key in validated.keys():
            if key not in arg_names:
                raise RuntimeError(
                    '"%s" keyword argument to @validate() decorator does not '
                    'match any arguments in the function signature of %s' %
                    (key, func)
                )

        # `wraps` preserves the function name etc...
        @wraps(func)
        def wrapper(*args, **kwargs):
            for idx, value in enumerate(args):
                key = arg_names[idx]
                kwargs[key] = value

            errors = {}
            for key, value in kwargs.items():
                if key in validated:
                    validator = validated[key]
                    try:
                        kwargs[key] = validator(value)
                    except ValidationError as exc:
                        errors[key] = exc.description

            if errors:
                raise ValidationError(errors)

            return func(**kwargs)

        # Preserve the function signature.
        copy_signature(func, wrapper)
        return wrapper

    return decorator
