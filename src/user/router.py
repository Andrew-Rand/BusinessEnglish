from typing import Any, Dict, Union
from uuid import UUID

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from src.basecore.error_handler import error_handler
from src.db.db_config import get_session
from src.user import api
from src.user.models import User
from src.user.serializers import Response, UserPostSchema, UserLoginRequest, RefreshTokenRequest, UserUpdateSchema, ChangePasswordRequest
from src.user.utils import login_required, get_user_id_from_header

router = APIRouter()


# CRUD for user
@router.get('/')
async def get_all_users(db_session: Session = Depends(get_session)) -> Dict[str, Any]:
    user_qs = api.get_user_list(db_session=db_session)
    return Response(code=200, status='Ok', message='Success', result=user_qs).dict(exclude_none=True)


@router.get('/user/{user_id}/')
async def get_user_by_id(user_id: UUID, db_session: Session = Depends(get_session)) -> Dict[str, Any]:
    user_obj = api.get_user_by_id(db_session=db_session, user_id=user_id)
    return Response(code=200, status='Ok', message='Success', result=user_obj).dict(exclude_none=True)


@router.put('/user/{user_id}/')
async def update_user(user_id: UUID, request: UserUpdateSchema, db_session: Session = Depends(get_session)) -> Dict[str, Any]:
    user_obj = api.update_user(
        db_session=db_session,
        user_id=user_id,
        username=request.username,
        email=request.email)
    return Response(code=200, status='Created', message='Success', result=user_obj).dict(exclude_none=True)


@router.post('/change_password')
@login_required
async def change_password(
        request: ChangePasswordRequest,
        Authorization: Union[str, None] = Header(default=None, convert_underscores=False),
        db_session: Session = Depends(get_session),
):

    print('ggg', Authorization)
    api.change_password(
        db_session=db_session,
        user_id=Authorization,
        password=request.password,
        new_password=request.new_password,
        new_password_repeated=request.new_password_repeated)

    return Response(code=201, status='Created', message='Success').dict(exclude_none=True)

@router.post('/signup/')
async def create_user(request: UserPostSchema, db_session: Session = Depends(get_session)) -> Dict[str, Any]:
    api.create_user(db_session=db_session, user=request.parameter)
    return Response(code=201, status='Created', message='Success').dict(exclude_none=True)


@router.post('/login/')
async def login(request: UserLoginRequest, db_session: Session = Depends(get_session)) -> Dict[str, Any]:
    print(request)
    response_data = api.login(db_session=db_session, user=request)
    return Response(code=200, status='Ok', message='Success', result=response_data).dict(exclude_none=True)


@router.post('/refresh/')
@login_required
async def refresh_token(request: RefreshTokenRequest, Authorization: Union[str, None] = Header(default=None, convert_underscores=False), db_session: Session = Depends(get_session)) -> Dict[str, Any]:
    response_data = api.refresh_token(db_session=db_session, refresh_token=request.refresh_token)
    return Response(code=200, status='Ok', message='Success', result=response_data).dict(exclude_none=True)
