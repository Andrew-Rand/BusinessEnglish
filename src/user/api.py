from typing import Dict

import jwt
from sqlalchemy.orm import Session, Query
from werkzeug.security import generate_password_hash, check_password_hash

from src.basecore.error_handler import BadRequestError, NotFoundError, NOT_FOUND_ERROR_MESSAGE, ForbiddenError
from src.user.constants import ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME, SECRET_KEY
from src.user.models import User
from src.user.serializers import UserSchema, UserLoginRequest, UserUpdateSchema
from src.user.utils import create_token
from src.user.validators import validate_password


def get_user_list(db_session: Session, skip: int = 0, limit: int = 100) -> Query:
    return db_session.query(User).offset(skip).limit(limit).all()


def get_user_by_id(db_session: Session, user_id: str) -> Query:

    user_obj = db_session.query(User).filter(User.id == user_id).first()

    if not user_obj:
        raise NotFoundError(NOT_FOUND_ERROR_MESSAGE)

    return user_obj


def create_user(db_session: Session, user: UserSchema) -> User:

    validate_password(field='password', value=user.password)
    hashed_password = generate_password_hash(password=user.password, method='sha256')
    user_obj = User(username=user.username, email=user.email, password=hashed_password)
    db_session.add(user_obj)
    db_session.commit()
    db_session.refresh(user_obj)

    return user_obj


def update_user(db_session: Session, user_id: str, update_data: UserUpdateSchema) -> User:

    user_obj = get_user_by_id(db_session=db_session, user_id=user_id)

    if not user_obj:
        raise NotFoundError(NOT_FOUND_ERROR_MESSAGE)

    user_obj.username = update_data.username if update_data.username else user_obj.username
    user_obj.email = update_data.email if update_data.email else user_obj.email
    user_obj.successed_tasks = update_data.successed_tasks if update_data.successed_tasks else user_obj.successed_tasks
    user_obj.streak = update_data.streak if update_data.streak else user_obj.streak
    db_session.commit()
    db_session.refresh(user_obj)

    return user_obj


def change_password(
        db_session: Session,
        user_id: str, password: str, new_password: str, new_password_repeated: str,
        *args, **kwargs
):

    user_obj = get_user_by_id(db_session=db_session, user_id=user_id)

    if not user_obj:
        raise NotFoundError(NOT_FOUND_ERROR_MESSAGE)

    if not check_password_hash(user_obj.password, password):
        raise Exception('Incorrect password')

    if not new_password == new_password_repeated:
        raise Exception('Write new password twice, please, check if they are equal')

    hashed_password = generate_password_hash(password=new_password, method='sha256')
    user_obj.password = hashed_password
    db_session.commit()
    db_session.refresh(user_obj)


def login(db_session: Session, user: UserLoginRequest) -> Dict[str, str]:
    print(user.email)
    user_obj = db_session.query(User).filter(User.email == user.email).first()

    if not user_obj:
        raise NotFoundError(NOT_FOUND_ERROR_MESSAGE)

    if not check_password_hash(user_obj.password, user.password):
        raise BadRequestError('Incorrect paassword')

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
        raise ForbiddenError('Refresh token is expired, go to the refresh endpoint')
    except jwt.InvalidTokenError:
        raise ForbiddenError('Invalid token. Please log in again')

    user_obj = db_session.query(User).filter(User.id == payload['id']).first()

    if not user_obj:
        raise NotFoundError(NOT_FOUND_ERROR_MESSAGE)

    access_token = create_token(str(user_obj.id), time_delta_seconds=ACCESS_TOKEN_LIFETIME)
    refresh_token = create_token(str(user_obj.id), time_delta_seconds=REFRESH_TOKEN_LIFETIME)

    response_data = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    return response_data
