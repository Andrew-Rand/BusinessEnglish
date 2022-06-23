from uuid import uuid4

from marshmallow import Schema, fields

from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from src.user.models import User


# TODO: Add validators to serializers

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


class UserSerializer(Schema):
    id = fields.Str(default=uuid4())
    username = fields.Str()
    password = fields.Str()
    email = fields.Str()
    successed_tasks = fields.Int(default=0)
    streak = fields.Int(default=0)


class UserUpdateSerializer(Schema):
    username = fields.Str(default=None)
    email = fields.Email(default=None)
    streak = fields.Int(default=None)
    successed_tasks = fields.Int(default=None)
    is_admin = fields.Bool(default=None)


class UserChangePasswordSerializer(Schema):
    password = fields.Str()
    new_password = fields.Str()
    new_password_repeated = fields.Str()


class UserLoginSerializer(Schema):
    email = fields.Email()
    password = fields.Str()


class UserRefreshTokenSerializer(Schema):
    refresh_token = fields.Str()
