from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starlette.responses import Response

from src.basecore.std_response import create_response
from src.db.db_config import get_session
from src.user import api
from src.user.serializers import UserSchemaSerializer, UserUpdateSerializer, UserChangePasswordSerializer, \
    UserLoginSerializer, UserRefreshTokenSerializer, UserSerializer
from src.user.utils import login_required


router = APIRouter()


# TODO: Rewrite with request serializers and handle validation errors

# CRUD for user
@router.get('/')
@login_required
async def get_all_users(request: Request, user_id: str = None, db_session: Session = Depends(get_session)) -> Response:

    # TODO: Add permission (Only for admin)
    response_serializer = UserSchemaSerializer()

    user_list = api.get_user_list(db_session=db_session)
    result = response_serializer.dump(obj=user_list, many=True)

    return create_response(code=200, status='Ok', message='Success', result=result)


@router.get('/user/')
@login_required
async def get_user_by_id(request: Request, user_id: str = None, db_session: Session = Depends(get_session)) -> Response:

    response_serializer = UserSchemaSerializer()

    user_obj = api.get_user_by_id(db_session=db_session, user_id=user_id)
    result = response_serializer.dump(user_obj)

    return create_response(code=200, status='Ok', message='Success', result=result)


@router.put('/user/')
@login_required
async def update_user(request: Request, user_id: str = None, db_session: Session = Depends(get_session)) -> Response:

    request_serializer = UserUpdateSerializer()
    response_serializer = UserSchemaSerializer()
    serialized_data = request_serializer.load(await request.json())

    user_obj = api.update_user(
        db_session=db_session,
        user_id=user_id,
        data=serialized_data
    )
    result = response_serializer.dump(user_obj)

    return create_response(code=200, status='Created', message='Success', result=result)


@router.post('/change_password/')
@login_required
async def change_password(
        request: Request,
        user_id: str = None,
        db_session: Session = Depends(get_session)
) -> Response:

    request_serializer = UserChangePasswordSerializer()
    serialized_data = request_serializer.load(await request.json())

    api.change_password(
        db_session=db_session,
        user_id=user_id,
        data=serialized_data
    )

    return create_response(code=201, status='Created', message='Success')


@router.post('/signup/')
async def create_user(request: Request, db_session: Session = Depends(get_session)) -> Response:

    request_serializer = UserSerializer()
    serialized_data = request_serializer.load(await request.json())

    api.create_user(db_session=db_session, data=serialized_data)

    return create_response(code=201, status='Created', message='Success')


@router.post('/login/')
async def login(request: Request, db_session: Session = Depends(get_session)) -> Response:

    request_serializer = UserLoginSerializer()
    serialized_data = request_serializer.load(await request.json())

    response_data = api.login(db_session=db_session, data=serialized_data)

    return create_response(code=200, status='Ok', message='Success', result=response_data)


@router.post('/refresh/')
async def refresh_token(request: Request, db_session: Session = Depends(get_session)) -> Response:

    request_serializer = UserRefreshTokenSerializer()
    serialized_data = request_serializer.load(await request.json())

    response_data = api.refresh_token(db_session=db_session, refresh_token=serialized_data['refresh_token'])

    return create_response(code=200, status='Ok', message='Success', result=response_data)
