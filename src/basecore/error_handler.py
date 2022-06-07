from typing import Callable, Any

from fastapi import HTTPException
from fastapi.routing import APIRoute
from pydantic import ValidationError
from starlette.requests import Request

from src.basecore.std_response import Response


def error_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args, **kwargs):
        try:
            print('aaa')
            return func(*args, **kwargs)
        except ValidationError as validation_error:
            print('bbb')
            return Response(code=400, status='Bad request', message='Error', result=validation_error).dict(exclude_none=True)
        except Exception as e:
            print('ccc')
            return Response(code=400, status='Bad request', message='Error', result=str(e)).dict(exclude_none=True)
    return wrapper


