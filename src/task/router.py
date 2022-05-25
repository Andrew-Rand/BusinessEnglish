from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db.db_config import get_session
from src.task import api
from src.task.serializers import TaskSchema, Response

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
async def create_task():
    pass


@router.get('/{task_id}/')
async def get_task_by_id(task_id: UUID):
    pass


@router.put('/{task_id}/')
async def update_task(task_id: UUID):
    pass


@router.delete('/{task_id}/')
async def delete_task(task_id: UUID):
    pass


# Check the task
@router.get('/get_random/')
async def get_random_task():
    pass


@router.get('/check_task/{task_id}/')
async def get_check_task(task_id: UUID):
    pass
