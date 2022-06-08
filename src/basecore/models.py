from uuid import uuid4

from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Date

from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from src.db.db_config import Base
from src.task.serializers import TaskType


class BaseModel(Base):
    __abstract__ = True
    map_datetime_formats_to_return = {}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    # TODO: Add created_at and updated_at fields
    # original_timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    # adjusted_timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

    class Meta:
        fields = ()

    # TODO: Create serializer for all qs to json and rm this methods

    def get_value(self, column):
        time_fields = [
            column.name
            for column in self.__table__.columns
            if isinstance(column.type, (DateTime, Date))
        ]

        if column in time_fields:
            return self.convert_datetime_into_string(column)

        return getattr(self, column)

    def as_dict(self, fields=None):
        if not fields:
            fields = self.Meta.fields or [
                column.name for column in self.__table__.columns
            ]

        return {column: self.get_value(column) for column in fields}