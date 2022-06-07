from enum import Enum
from typing import List, Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel


class TaskType(int, Enum):
    russian_to_english = 1
    english_to_russian = 2
    join_phrase = 3


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


class Response(GenericModel):
    # TODO: Move it to basecore response schema
    code: str
    status: str
    message: str
    result: Any


class CheckResponse(BaseModel):
    answer: str
