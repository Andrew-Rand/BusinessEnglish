from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.postgresql import ARRAY

from src.basecore.models import BaseModel
from src.task.serializers import TaskType


class Task(BaseModel):

    __tablename__ = 'tasks'

    type = Column(Enum(TaskType))
    question = Column(ARRAY(item_type=String, as_tuple=False, dimensions=None, zero_indexes=True))
    answer = Column(ARRAY(item_type=String, as_tuple=False, dimensions=None, zero_indexes=True))

    def __repr__(self):
        return f'Task id: {self.id}, type: {self.type}'
