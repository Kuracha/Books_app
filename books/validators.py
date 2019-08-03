from django.core.exceptions import ValidationError

from datetime import date


def check_if_value_is_negative(value):
    if value < 0:
        raise ValidationError("Value can't be negative")
    else:
        return value


MONTHS = ("01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12")

DAYS = ("01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16",
              "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31")


def check_if_value_is_date(value):
    if len(value) == 10:
        for i in range(0, 4):
            if not value[i].isdecimal():
                raise ValidationError("Your year can contain only a numbers ")

        if value[4] != "-":
            raise ValidationError("Your date can have only such a structure: yyyy-mm-dd or yyyy")

        for i in range(5, 7):
            if not value[i].isdecimal():
                raise ValidationError("your month can contain only a numbers")

        if value[5:7] not in MONTHS:
            raise ValidationError("your month can have value only from 1 to 12")

        if value[7] != "-":
            raise ValidationError("Your date can have only such a structure: yyyy-mm-dd or yyyy")

        for i in range(8, 10):
            if not value[i].isdecimal():
                raise ValidationError("your day can contain only a numbers")

        if value[8:10] not in DAYS:
            raise ValidationError("your day can have value only from 1 to 31")
        return value

    elif len(value) == 4:
        for i in range(0, 4):
            if not value[i].isdecimal():
                raise ValidationError("Your year can contain only a numbers ")
        return value

    else:
        raise ValidationError("Your date can have only such a structure: yyyy-mm-dd or yyyy")


def max_year_validator(value):
    if value.isdecimal():
        current_date = date.today()
        max_year = int(current_date.year) + 5
        if int(value[0:4]) > max_year:
            raise ValidationError(f'Highest date you can input is {max_year}')
        return value
