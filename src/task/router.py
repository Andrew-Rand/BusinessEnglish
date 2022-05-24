from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter

from src.task.serializers import Task

router = APIRouter()


#TODO: create nested functions from each endpoint and move it to the api.py


@router.post('/{task_id}')
async def update_item(task_id: UUID, task: Task) -> Dict[str, Any]:
    return {'question': task.question, 'answer': task.answer}
