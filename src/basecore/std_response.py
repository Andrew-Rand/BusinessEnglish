import json
from typing import Any, Union, Dict, Optional, List

from pydantic.generics import GenericModel
from starlette.responses import Response as std_response
from fastapi.responses import ORJSONResponse as json_response


class Response(GenericModel):
    code: str
    status: str
    message: str
    result: Any


def create_response(code: int, status: str, message: str, result: Any = None) -> json_response:
    content = Response(code=code, status=status, message=message, result=result).dict(exclude_none=True)
    return json_response(content=content, status_code=code)
