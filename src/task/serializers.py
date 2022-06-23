from uuid import uuid4

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import Schema, fields

from src.task.models import Task


class TaskSchemaSerializer(SQLAlchemyAutoSchema):
    # Only for testing marshmellow-sqlalchemy autoschema, you can use only TaskSerializer
    class Meta:
        model = Task
        # include_relationships = True
        load_instance = True  # Optional: deserialize to model instances


class TaskSerializer(Schema):
    id = fields.UUID(default=uuid4())
    type = fields.Int()
    question = fields.List(cls_or_instance=fields.Str)
    answer = fields.List(cls_or_instance=fields.Str)


class TaskUpdateSerializer(Schema):
    question = fields.List(cls_or_instance=fields.Str)
    answer = fields.List(cls_or_instance=fields.Str)


class TaskCheckSerializer(Schema):
    answer = fields.Str()
