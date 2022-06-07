import json
from functools import wraps
from typing import Callable, Any

from fastapi.routing import APIRoute, APIRouter
from starlette.requests import Request
from pydantic import ValidationError

from src.basecore.std_response import Response
from starlette.responses import Response as error_response


class BadRequestError(Exception):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(args)


class ForbiddenError(Exception):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(args)


class NotAuthorizedError(Exception):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(args)


class NotFoundError(Exception):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(args)


class TeapotError(Exception):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(args)


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        print('Middleware')
        return await call_next(request)
    except Exception as e:
        print('Exception')
        return error_response(content=json.dumps(Response(code=400, status='Bad request', message='Error', result=str(e)).dict(exclude_none=True)), status_code=400)
