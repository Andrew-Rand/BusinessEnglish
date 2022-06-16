from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from src.db.db_config import Base


class BaseModel(Base):
    __abstract__ = True
    map_datetime_formats_to_return = {}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    # TODO: Add created_at and updated_at fields
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)

    class Meta:
        fields = ()
