from typing import Union, List
from uuid import UUID, uuid4
from enum import Enum

from pydantic import BaseModel


class TaskType(int, Enum):
    russian_to_english = 1
    english_to_russian = 2


class Task(BaseModel):
    """To add a type of field, you need to use typehint after :. If you want to add a default value, use ="""
    id: UUID = uuid4
    type: TaskType
    russian: Union[str, List]
    english: Union[str, List]

