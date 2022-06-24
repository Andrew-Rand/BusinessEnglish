from uuid import UUID

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.basecore.std_response import create_response
from src.db.db_config import get_session
from src.task import api
from src.task.serializers import TaskSchemaSerializer, TaskSerializer, TaskUpdateSerializer, TaskCheckSerializer
from starlette.responses import Response

from src.user.utils import login_required

router = APIRouter()


# TODO: Rewrite with request serializers and handle validation errors


# CRUD for task
@router.get('/')
async def get_all_tasks(db_session: Session = Depends(get_session)) -> Response:

    response_serializer = TaskSerializer()

    task_list = api.get_task_list(db_session=db_session)
    result = response_serializer.dump(obj=task_list, many=True)

    return create_response(code=200, status='Ok', message='Success', result=result)


@router.post('/')
async def create_task(request: Request, db_session: Session = Depends(get_session)) -> Response:

    request_serializer = TaskSerializer()
    serialized_data = request_serializer.load(await request.json())

    api.create_task(db_session=db_session, data=serialized_data)

    return create_response(code=201, status='Created', message='Success')


@router.get('/task/{task_id}/')
async def get_task_by_id(task_id: UUID, db_session: Session = Depends(get_session)) -> Response:

    response_serializer = TaskSchemaSerializer()

    task_obj = api.get_task_by_id(db_session=db_session, task_id=task_id)
    result = response_serializer.dump(task_obj)

    return create_response(code=200, status='Ok', message='Success', result=result)


@router.put('/task/{task_id}/')
async def update_task(task_id: UUID, request: Request, db_session: Session = Depends(get_session)) -> Response:

    request_serializer = TaskUpdateSerializer()
    response_serializer = TaskSchemaSerializer()
    serialized_data = request_serializer.load(await request.json())

    task_obj = api.update_task(
        db_session=db_session,
        task_id=task_id,
        data=serialized_data
    )
    result = response_serializer.dump(task_obj)

    return create_response(code=200, status='Created', message='Success', result=result)


@router.delete('/task/{task_id}/')
async def delete_task(task_id: UUID, db_session: Session = Depends(get_session)) -> Response:

    api.remove_task(db_session=db_session, task_id=task_id)

    return create_response(code=200, status='Ok', message='Success')


# Check the task endpoints
@router.get('/get_random/')
async def get_random_task(db_session: Session = Depends(get_session)) -> Response:

    response_serializer = TaskSchemaSerializer()

    task_obj = api.get_random_task(db_session=db_session)
    result = response_serializer.dump(task_obj)

    return create_response(code=200, status='Ok', message='Success', result=result)


@router.post('/check_task/{task_id}/')
@login_required
async def check_task(
        task_id: UUID,
        request: Request,
        user_id: str = None,
        db_session: Session = Depends(get_session)
) -> Response:

    request_serializer = TaskCheckSerializer()
    serialized_data = request_serializer.load(await request.json())

    if api.check_task(db_session=db_session, task_id=task_id, answer=serialized_data['answer'], user_id=user_id):
        return create_response(code=200, status='Ok', message='Success')
    else:
        return create_response(code=200, status='Wrong answer', message='Try again')
