import json
from enum import Enum
from typing import List, Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

from sqlalchemy.ext.declarative import DeclarativeMeta


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


class CheckResponse(BaseModel):
    answer: str


class AlchemyEncoder(json.JSONEncoder):

    SERVICE = {'metadata', 'Meta', "as_dict", "map_datetime_formats_to_return", "get_value", "registry"}

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # start with a sqlalchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x not in self.SERVICE]:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    if field == 'id':
                        fields[field] = str(data)
                    else:
                        fields[field] = None
            # finish with a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
