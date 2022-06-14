from typing import List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.task.constants import TaskType
from src.task.models import Task


class TaskSchema(BaseModel):
    """To add a type of field, you need to use typehint after :. If you want to add a default value, use ="""
    id: UUID = uuid4()
    type: TaskType
    question: List[str]
    answer: List[str]

    class Config:
        orm_mode = True


class RequestTask(BaseModel):
    parameter: TaskSchema = Field(...)


class CheckResponse(BaseModel):
    answer: str


class TaskSchemaSerializer(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_relationships = True
        load_instance = True  # Optional: deserialize to model instances
