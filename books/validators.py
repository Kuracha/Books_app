from django.core.exceptions import ValidationError

from datetime import date


def check_if_value_is_negative(value):
    if value < 0:
        raise ValidationError("Value can't be negative")
    else:
        return value


def max_year_validator(value):
    current_date = date.today()
    max_year = int(current_date.year) + 2
    if value > max_year:
        raise ValidationError(f'Highest date you can input is {max_year}')
    else:
        return value
