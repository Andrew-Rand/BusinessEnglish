import datetime
from functools import wraps
from typing import Callable, Any, Union

from fastapi import Header, Request
import jwt
from sqlalchemy.orm import Session

from src.basecore.error_handler import ForbiddenError, NotFoundError
from src.basecore.std_response import Response
from src.db.db_config import get_session
from src.user.constants import SECRET_KEY
from src.user.models import User


def create_token(user_id: str, time_delta_seconds: int) -> str:

    token_payload = {
        'id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=time_delta_seconds),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')
    return token


def login_required(func: Any) -> Any:
    @wraps(func)
    async def wrapper(authorization: Union[str, None] = None, *args: Any, **kwargs: Any) -> Any:
        # TODO: Move strings messages to constants
        print(
            authorization
        )
        if not authorization:
            raise ForbiddenError('Token is missing')
        try:
            payload = jwt.decode(authorization, SECRET_KEY, algorithms=['HS256'])
            print('aaa', payload)
        except jwt.ExpiredSignatureError:
            raise ForbiddenError('Access token is expired, go to the refresh endpoint')
        except jwt.InvalidTokenError as e:
            print(e)
            raise ForbiddenError('Invalid token. Please log in again')

        with get_session() as session:
            user_obj = session.query(User).filter(User.id == payload['id']).first()

            if user_obj is None:
                raise NotFoundError('User is not found')

            print(user_obj.id)

        return await func(authorization=str(user_obj.id), *args, **kwargs)

    return wrapper

