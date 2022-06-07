import json
from typing import Any

from pydantic.generics import GenericModel
from starlette.responses import Response as std_response


class Response(GenericModel):
    code: str
    status: str
    message: str
    result: Any


def create_response(code: int, status: str, message: str, result: Any) -> Response:
    content = json.dumps(Response(code=code, status=status, message=message, result=result).dict(exclude_none=True))
    return std_response(content=content, status_code=code)
