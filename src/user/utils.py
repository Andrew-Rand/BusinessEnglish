import datetime
from functools import wraps
from typing import Callable, Any, Union

from fastapi import Header, Request
import jwt
from sqlalchemy.orm import Session

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
    async def wrapper(Authorization: Union[str, None] = None, *args: Any, **kwargs: Any) -> Any:
        # TODO: Move strings messages to constants
        print(
            Authorization
        )
        if not Authorization:
            return Response(code=403, status='Forbidden', message='Token is missing').dict(exclude_none=True)
        try:
            payload = jwt.decode(Authorization, SECRET_KEY, algorithms=['HS256'])
            print('aaa', payload)
        except jwt.ExpiredSignatureError:
            return Response(code=403, status='Forbidden', message='Access token is expired, go to the refresh endpoint').dict(exclude_none=True)
        except jwt.InvalidTokenError as e:
            print(e)
            return Response(code=403, status='Forbidden', message='Invalid token. Please log in again').dict(exclude_none=True)

        with get_session() as session:
            user_obj = session.query(User).filter(User.id == payload['id']).first()

            if user_obj is None:
                raise Exception('User not found')

            print(user_obj.id)

        return await func(Authorization=str(user_obj.id), *args, **kwargs)

    return wrapper


def get_user_id_from_header(header: str):
    with get_session() as session:
        print('fff', header)
        payload = jwt.decode(header, SECRET_KEY, algorithms=['HS256'])
        user_obj = session.query(User).filter(User.id == payload['id']).first()
        return(str(user_obj.id))
