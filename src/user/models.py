from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.orm import validates

from src.basecore.models import BaseModel
from src.user.validators import validate_name, validate_positive_number, validate_email


class User(BaseModel):

    __tablename__ = 'users'

    username = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(200))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    successed_tasks = Column(Integer, default=0)
    streak = Column(Integer, default=0)

    @validates('username')
    def validate_username(self, field, value):
        validate_name(field=field, value=value)
        return value

    @validates('email')
    def validate_email(self, field, value):
        validate_email(field=field, value=value)
        return value

    @validates('successed_tasks')
    def validate_successed_tasks(self, field, value):
        validate_positive_number(field=field, value=value)
        return value

    @validates('streak')
    def validate_streak(self, field, value):
        validate_positive_number(field=field, value=value)
        return value

    def __repr__(self):
        return f'User id: {self.id}'

# TODO: Add achivemens for user
