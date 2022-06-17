from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base


base = declarative_base()


class BaseModel(base):
    __abstract__ = True
    map_datetime_formats_to_return = {}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

    class Meta:
        fields = ()
