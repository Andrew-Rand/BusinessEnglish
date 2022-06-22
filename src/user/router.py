from typing import Union

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from starlette.responses import Response

from src.basecore.std_response import create_response
from src.db.db_config import get_session
from src.user import api
from src.user.serializers import UserLoginRequest, RefreshTokenRequest, UserUpdateSchema, \
    ChangePasswordRequest, UserSchemaSerializer, UserSchema
from src.user.utils import login_required

router = APIRouter()


# TODO: Rewrite with request serializers and handle validation errors

# CRUD for user
@router.get('/')
@login_required
async def get_all_users(
        authorization: Union[str, None] = Header(default=None, convert_underscores=False),
        db_session: Session = Depends(get_session)
) -> Response:

    # TODO: Add permission (Only for admin)
    serializer = UserSchemaSerializer()
    user_list = api.get_user_list(db_session=db_session)
    result = serializer.dump(obj=user_list, many=True)

    return create_response(code=200, status='Ok', message='Success', result=result)


@router.get('/user/')
@login_required
async def get_user_by_id(
        authorization: Union[str, None] = Header(default=None, convert_underscores=False),
        db_session: Session = Depends(get_session)
) -> Response:

    serializer = UserSchemaSerializer()
    user_obj = api.get_user_by_id(db_session=db_session, user_id=authorization)
    result = serializer.dump(user_obj)

    return create_response(code=200, status='Ok', message='Success', result=result)


@router.put('/user/')
@login_required
async def update_user(
        request: UserUpdateSchema,
        authorization: Union[str, None] = Header(default=None, convert_underscores=False),
        db_session: Session = Depends(get_session)
) -> Response:

    serializer = UserSchemaSerializer()
    user_obj = api.update_user(
        db_session=db_session,
        user_id=authorization,
        username=request.username,
        email=request.email)
    result = serializer.dump(user_obj)
    return create_response(code=200, status='Created', message='Success', result=result)


@router.post('/change_password')
@login_required
async def change_password(
        request: ChangePasswordRequest,
        authorization: Union[str, None] = Header(default=None, convert_underscores=False),
        db_session: Session = Depends(get_session),
) -> Response:

    api.change_password(
        db_session=db_session,
        user_id=authorization,
        password=request.password,
        new_password=request.new_password,
        new_password_repeated=request.new_password_repeated)

    return create_response(code=201, status='Created', message='Success')


@router.post('/signup/')
async def create_user(request: UserSchema, db_session: Session = Depends(get_session)) -> Response:
    api.create_user(db_session=db_session, user=request)
    return create_response(code=201, status='Created', message='Success')


@router.post('/login/')
async def login(request: UserLoginRequest, db_session: Session = Depends(get_session)) -> Response:
    response_data = api.login(db_session=db_session, user=request)
    return create_response(code=200, status='Ok', message='Success', result=response_data)


@router.post('/refresh/')
@login_required
async def refresh_token(
        request: RefreshTokenRequest,
        authorization: Union[str, None] = Header(default=None, convert_underscores=False),
        db_session: Session = Depends(get_session)
) -> Response:

    response_data = api.refresh_token(db_session=db_session, refresh_token=request.refresh_token)
    return create_response(code=200, status='Ok', message='Success', result=response_data)
