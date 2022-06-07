from random import choice
from typing import List, Dict
from uuid import UUID

import jwt
from sqlalchemy.orm import Session, Query
from werkzeug.security import generate_password_hash, check_password_hash

from src.basecore.error_handler import error_handler
from src.constants import ENCODE_FORMAT
from src.user.constants import ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME, SECRET_KEY
from src.user.models import User
from src.user.serializers import UserSchema, UserLoginRequest
from src.user.utils import create_token
from src.user.validators import validate_password


def get_user_list(db_session: Session, skip: int = 0, limit: int = 100) -> Query:
    return db_session.query(User).offset(skip).limit(limit).all()


def get_user_by_id(db_session: Session, user_id: UUID) -> Query:
    return db_session.query(User).filter(User.id == user_id).first()


def create_user(db_session: Session, user: UserSchema) -> User:

    validate_password(field='password', value=user.password)
    hashed_password = generate_password_hash(password=user.password, method='sha256')

    user_obj = User(username=user.username, email=user.email, password=hashed_password)
    db_session.add(user_obj)
    db_session.commit()
    db_session.refresh(user_obj)
    return user_obj


def login(db_session: Session, user: UserLoginRequest) -> Dict[str, str]:
    user_obj = db_session.query(User).filter(User.email == user.email).first()
    if check_password_hash(user_obj.password, user.password):
        user_id = str(user_obj.id)
        access_token = create_token(user_id, time_delta_seconds=ACCESS_TOKEN_LIFETIME)
        refresh_token = create_token(user_id, time_delta_seconds=REFRESH_TOKEN_LIFETIME)

        response_data = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

        return response_data


def refresh_token(db_session: Session, refresh_token: str) -> Dict[str, str]:
    # TODO: Add custom errors in this case
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise Exception('expired refresh token, please login again.')
    except jwt.DecodeError:
        raise Exception('token data is incorrect')

    print('aaa', payload['id'])

    user_obj = db_session.query(User).filter(User.id == payload['id']).first()
    if user_obj is None:
        raise Exception('User not found')

    access_token = create_token(str(user_obj.id), time_delta_seconds=ACCESS_TOKEN_LIFETIME)
    refresh_token = create_token(str(user_obj.id), time_delta_seconds=REFRESH_TOKEN_LIFETIME)

    response_data = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    return response_data
