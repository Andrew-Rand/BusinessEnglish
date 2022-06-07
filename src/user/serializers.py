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


class UserLoginRequest(BaseModel):
    email: str
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class Response(GenericModel):
    # TODO: Move it to basecore response schema
    code: str
    status: str
    message: str
    result: Any
