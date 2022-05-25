from re import match

from pydantic import ValidationError


def validate_name(field: str, value: str) -> None:
    reg_ex = r'^[a-zA-z]+$'
    if not match(reg_ex, value):
        raise ValidationError(f'{value} is not a name, please use only A-z letters for {field}')


def validate_positive_number(field: str, value: int) -> None:
    if value < 0:
        raise ValidationError(f'{field}: value must be positive')


def validate_email(field: str, value: str) -> None:
    reg_ex = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    if not match(reg_ex, value):
        raise ValidationError(f'{value} for {field} must be an email: example@engmail.com')


def validate_password(field: str, value: str) -> None:
    reg_ex = r'(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{10,}'
    """ (?=.*[0-9]) - contains at least one number;
        (?=.*[!@#$%^&*]) - contains at least one spec char;
        (?=.*[a-z]) - contains at least one lowercase Latin letter;
        (?=.*[A-Z]) - contains at least one uppercase Latin letter;
        [0-9a-zA-Z!@#$%^&*]{10,} - contains at least 10 of all this symbols.
    """
    if not match(reg_ex, value):
        raise ValidationError(f'{value} for {field} must be 8 and contains at least'
                              f' number, lowercase and upper case, spec char')