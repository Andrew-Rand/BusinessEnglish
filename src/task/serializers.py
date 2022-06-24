from uuid import uuid4

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import Schema, fields, validate

from src.task.constants import TaskType
from src.task.models import Task


class TaskSchemaSerializer(SQLAlchemyAutoSchema):
    """You can use only TaskSerializer, but auto schema is pretty convenient for response serializer"""
    class Meta:
        model = Task
        # include_relationships = True  # uncomment the string if you need to serialize related tables
        # load_instance = True  # uncomment the string if you need to use the class as request serializer


class TaskSerializer(Schema):
    id = fields.UUID(default=uuid4())
    type = fields.Int(validate=validate.OneOf([e.value for e in TaskType]))
    question = fields.List(cls_or_instance=fields.Str)
    answer = fields.List(cls_or_instance=fields.Str)


class TaskUpdateSerializer(Schema):
    question = fields.List(cls_or_instance=fields.Str)
    answer = fields.List(cls_or_instance=fields.Str)


class TaskCheckSerializer(Schema):
    answer = fields.Str()
