from typing import Any

from pydantic.generics import GenericModel


class Response(GenericModel):
    code: str
    status: str
    message: str
    result: Any
