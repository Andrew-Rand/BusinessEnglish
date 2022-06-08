from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel


class UserSchema(BaseModel):
    id: UUID = uuid4()
    username: str
    email: str
    password: str
    is_active: bool = True
    is_admin: bool = False
    successed_tasks: int = 0
    streak: int = 0

    class Config:
        orm_mode = True


class UserPostSchema(BaseModel):
    parameter: UserSchema = Field(...)


class UserUpdateSchema(BaseModel):
    username: str = None
    email: str = None
    is_admin: bool = False


class UserLoginRequest(BaseModel):
    email: str
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class ChangePasswordRequest(BaseModel):
    password: str
    new_password: str
    new_password_repeated: str

