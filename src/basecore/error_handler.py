from typing import Any

from sqlalchemy.exc import IntegrityError
from starlette.requests import Request
from pydantic import ValidationError

from src.basecore.std_response import create_response


NOT_FOUND_ERROR_MESSAGE = "Requested object doesn't exist"


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
    except (
            ValidationError,
            NotFoundError,
            IntegrityError,
            BadRequestError
    ) as client_error:
        return create_response(code=400, status='Bad request', message=str(client_error))
    except ForbiddenError as auth_error:
        return create_response(code=403, status='Bad request', message=str(auth_error))
    except Exception as e:
        print('Exception')
        return create_response(code=500, status='Bad request', message='Error', result=str(e))
