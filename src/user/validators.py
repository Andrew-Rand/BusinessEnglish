from re import match

NAME_REG_EXP = r'^[a-zA-z]+$'
EMAIL_REG_EXP = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
PASSWORD_REG_EXP = r'(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{8,}'
""" (?=.*[0-9]) - contains at least one number;
    (?=.*[!@#$%^&*]) - contains at least one spec char;
    (?=.*[a-z]) - contains at least one lowercase Latin letter;
    (?=.*[A-Z]) - contains at least one uppercase Latin letter;
    [0-9a-zA-Z!@#$%^&*]{10,} - contains at least 10 of all this symbols.
"""


def validate_name(field: str, value: str) -> None:
    if not match(NAME_REG_EXP, value):
        raise ValueError(f'{value} is not a name, please use only A-z letters for {field}')


def validate_positive_number(field: str, value: int) -> None:
    if value < 0:
        raise ValueError(f'{field}: value must be positive')


def validate_email(field: str, value: str) -> None:
    if not match(EMAIL_REG_EXP, value):
        raise ValueError(f'{value} for {field} must be an email: example@engmail.com')


def validate_password(field: str, value: str) -> None:
    if not match(PASSWORD_REG_EXP, value):
        raise ValueError(f'{value} for {field} must be 8 and contains at least number,'
                         f' lowercase and upper case, spec char')
