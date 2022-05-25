from uuid import uuid4

from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from src.db.db_config import Base
from src.task.serializers import TaskType


class Task(Base):

    __tablename__ = 'tasks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    type = Column(Enum(TaskType))
    question = Column(ARRAY(item_type=String, as_tuple=False, dimensions=None, zero_indexes=True))
    answer = Column(ARRAY(item_type=String, as_tuple=False, dimensions=None, zero_indexes=True))

    def __repr__(self):
        return f'Task id: {self.id}, type: {self.type}'
