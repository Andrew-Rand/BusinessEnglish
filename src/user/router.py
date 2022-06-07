from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.basecore.error_handler import error_handler
from src.db.db_config import get_session
from src.user import api
from src.user.serializers import Response, UserPostSchema, UserLoginRequest, RefreshTokenRequest

router = APIRouter()


# CRUD for user
@router.get('/')
async def get_all_users(db_session: Session = Depends(get_session)) -> Dict[str, Any]:
    user_qs = api.get_user_list(db_session=db_session)
    return Response(code=200, status='Ok', message='Success', result=user_qs).dict(exclude_none=True)


@router.get('/user/{user_id}/')
async def get_user_by_id(user_id: UUID, db_session: Session = Depends(get_session)) -> Dict[str, Any]:
    user_obj = api.get_user_by_id(db_session=db_session, task_id=user_id)
    return Response(code=200, status='Ok', message='Success', result=user_obj).dict(exclude_none=True)


@router.post('/signup/')
async def create_task(request: UserPostSchema, db_session: Session = Depends(get_session)) -> Dict[str, Any]:
    api.create_user(db_session=db_session, user=request.parameter)
    return Response(code=201, status='Created', message='Success').dict(exclude_none=True)


@router.post('/login/')
async def get_user_by_id(request: UserLoginRequest, db_session: Session = Depends(get_session)) -> Dict[str, Any]:
    response_data = api.login(db_session=db_session, user=request)
    return Response(code=200, status='Ok', message='Success', result=response_data).dict(exclude_none=True)


@router.post('/refresh/')
async def refresh_token(request: RefreshTokenRequest, db_session: Session = Depends(get_session)) -> Dict[str, Any]:
    response_data = api.refresh_token(db_session=db_session, refresh_token=request.refresh_token)
    return Response(code=200, status='Ok', message='Success', result=response_data).dict(exclude_none=True)



