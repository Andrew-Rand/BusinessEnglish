import json
from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.serializer import dumps


from src.basecore.std_response import create_response
from src.db.db_config import get_session
from src.task import api
from src.task.serializers import TaskSchema, RequestTask, CheckResponse, AlchemyEncoder
from starlette.responses import Response

router = APIRouter()

# TODO: Create serializer and rm as_dict usage


# CRUD for task
@router.get('/')
async def get_all_tasks(db_session: Session = Depends(get_session)) -> Response:
    task_list = api.get_task_list(db_session=db_session)
    return create_response(code=200, status='Ok', message='Success', result=task_list)


@router.post('/')
async def create_task(request: RequestTask, db_session: Session = Depends(get_session)) -> Response:
    api.create_task(db_session=db_session, task=request.parameter)
    return create_response(code=201, status='Created', message='Success')


@router.get('/task/{task_id}/')
async def get_task_by_id(task_id: UUID, db_session: Session = Depends(get_session)) -> Response:
    task_obj = api.get_task_by_id(db_session=db_session, task_id=task_id)
    return create_response(code=200, status='Ok', message='Success', result=task_obj.as_dict())


@router.put('/task/{task_id}/')
async def update_task(task_id: UUID, request: RequestTask, db_session: Session = Depends(get_session)) -> Response:
    task_obj = api.update_task(
        db_session=db_session,
        task_id=task_id,
        question=request.parameter.question,
        answer=request.parameter.answer)
    return create_response(code=200, status='Created', message='Success', result=task_obj.as_dict())


@router.delete('/task/{task_id}/')
async def delete_task(task_id: UUID, db_session: Session = Depends(get_session)) -> Response:
    api.remove_task(db_session=db_session, task_id=task_id)
    return create_response(code=200, status='Ok', message='Success')


# Check the task endpoints
@router.get('/get_random/')
async def get_random_task(db_session: Session = Depends(get_session)) -> Response:
    task_obj = api.get_random_task(db_session=db_session)
    return create_response(code=200, status='Ok', message='Success', result=task_obj.as_dict())


@router.post('/check_task/{task_id}/')
async def check_task(task_id: UUID, request: CheckResponse, db_session: Session = Depends(get_session)) -> Response:
    if api.check_task(db_session=db_session, task_id=task_id, answer=request.answer):
        return create_response(code=200, status='Ok', message='Success')
    else:
        return create_response(code=200, status='Wrong answer', message='Try again')
