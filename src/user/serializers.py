from uuid import uuid4

from marshmallow import Schema, fields, validate

from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from src.user.models import User


from src.user.validators import NAME_REG_EXP, PASSWORD_REG_EXP


class UserSchemaSerializer(SQLAlchemySchema):
    """You can use only UserSerializer, but auto schema is pretty convenient for response serializer"""
    class Meta:
        model = User
        # include_relationships = True  # uncomment the string if you need to serialize related tables
        # load_instance = True  # uncomment the string if you need to use the class as request serializer

    id = auto_field()
    username = auto_field()
    email = auto_field()
    successed_tasks = auto_field()
    streak = auto_field()


# TODO: Add base serializer

class UserSerializer(Schema):
    id = fields.Str(default=uuid4())
    username = fields.Str(validate=validate.Regexp(regex=NAME_REG_EXP))
    password = fields.Str(validate=validate.Regexp(regex=PASSWORD_REG_EXP))
    email = fields.Str(validate=validate.Email())  # Email field validate email, but for example
    successed_tasks = fields.Int(default=0, validate=validate.Range(min=0, min_inclusive=True))
    streak = fields.Int(default=0, validate=validate.Range(min=0, min_inclusive=True))
    is_admin = fields.Bool(default=None, validate=validate.OneOf([True, False]))


class UserUpdateSerializer(Schema):
    username = fields.Str(default=None, validate=validate.Regexp(regex=NAME_REG_EXP))
    email = fields.Email(default=None, validate=validate.Email())
    streak = fields.Int(default=None, validate=validate.Range(min=0, min_inclusive=True))
    successed_tasks = fields.Int(default=None, validate=validate.Range(min=0, min_inclusive=True))
    is_admin = fields.Bool(default=None, validate=validate.OneOf([True, False]))


class UserChangePasswordSerializer(Schema):
    password = fields.Str(validate=validate.Regexp(regex=PASSWORD_REG_EXP))
    new_password = fields.Str(validate=validate.Regexp(regex=PASSWORD_REG_EXP))
    new_password_repeated = fields.Str(validate=validate.Regexp(regex=PASSWORD_REG_EXP))


class UserLoginSerializer(Schema):
    email = fields.Email()
    password = fields.Str(validate=validate.Regexp(regex=PASSWORD_REG_EXP))


class UserRefreshTokenSerializer(Schema):
    refresh_token = fields.Str()
