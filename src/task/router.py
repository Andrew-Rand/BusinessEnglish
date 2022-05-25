from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.db_config import get_session
from src.task import api
from src.task.serializers import TaskSchema, Response, RequestTask, CheckResponse

router = APIRouter()


# TODO: create nested functions from each endpoint and move it to the api.py


@router.post('/tets/{task_id}')
# just a test, rm in the future
async def update_item(task_id: UUID, task: TaskSchema) -> Dict[str, Any]:
    return {'question': task.question, 'answer': task.answer}


# CRUD for task
@router.get('/')
async def get_all_tasks(db_session: Session = Depends(get_session)) -> Dict[str, Any]:
    task_qs = api.get_task_list(db_session=db_session)
    return Response(code=200, status='Ok', message='Success', result=task_qs).dict(exclude_none=True)


@router.post('/')
async def create_task(request: RequestTask, db_session: Session = Depends(get_session)) -> Dict[str, Any]:
    api.create_task(db_session=db_session, task=request.parameter)
    return Response(code=201, status='Created', message='Success').dict(exclude_none=True)


@router.get('/task/{task_id}/')
async def get_task_by_id(task_id: UUID, db_session: Session = Depends(get_session)) -> Dict[str, Any]:
    task_obj = api.get_task_by_id(db_session=db_session, task_id=task_id)
    return Response(code=200, status='Ok', message='Success', result=task_obj).dict(exclude_none=True)


@router.put('/task/{task_id}/')
async def update_task(task_id: UUID, request: RequestTask, db_session: Session = Depends(get_session)) -> Dict[str, Any]:
    task_obj = api.update_task(
        db_session=db_session,
        task_id=task_id,
        question=request.parameter.question,
        answer=request.parameter.answer)
    return Response(code=200, status='Created', message='Success', result=task_obj).dict(exclude_none=True)


@router.delete('/task/{task_id}/')
async def delete_task(task_id: UUID, db_session: Session = Depends(get_session)) -> Dict[str, Any]:
    api.remove_task(db_session=db_session, task_id=task_id)
    return Response(code=200, status='Ok', message='Success').dict(exclude_none=True)


# Check the task endpoints
@router.get('/get_random/')
async def get_random_task(db_session: Session = Depends(get_session)) -> Dict[str, Any]:
    task_obj = api.get_random_task(db_session=db_session)
    return Response(code=200, status='Ok', message='Success', result=task_obj).dict(exclude_none=True)


@router.get('/check_task/{task_id}/')
async def check_task(task_id: UUID, request: CheckResponse, db_session: Session = Depends(get_session)) -> Dict[str, Any]:
    if api.check_task(db_session=db_session, task_id=task_id, answer=request.answer):
        return Response(code=200, status='Ok', message='Success').dict(exclude_none=True)
    else:
        return Response(code=400, status='Bad request', message='Fail').dict(exclude_none=True)
