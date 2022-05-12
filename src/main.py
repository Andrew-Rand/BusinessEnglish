from typing import Dict, Any, List
from uuid import uuid4, UUID

from fastapi import FastAPI, HTTPException

from src.constants import STATUSES
from src.models import Task, TaskType, TaskUpdateRequest
from src.utils import std_response


app = FastAPI()  # initial web application
"""
    You can rung this application locally with terminal command:
        uvicorn src.main:app --reload
    Optional use --reload for debugging.
    
    Also you can work with app with Docker
    
    Use
    http://127.0.0.1:8000/docs
    to check avilable endpoints
"""

#fake database with fake task
db: List[Task] = [
    Task(
        id="691ce00a-490e-4c9c-938e-76f9044a8af4",
        type=TaskType.russian_to_english,
        question=['привет'],
        answer=['hi', 'hello']
    ),
    Task(
        id="2cf66c85-43bb-4553-94e4-583e9790a60f",
        type=TaskType.english_to_russian,
        answer=['привет', 'здравствуйте'],
        question=['hi']
    ),
    Task(
        id="2cf66c85-43bb-4553-94e4-583e9790a60f",
        type=TaskType.join_phrase,
        answer=['could you repeat please'],
        question=['could', 'you', 'repeat', 'please']
    ),
]

# Endpoint's system


@app.get('/')  # root endpoint
async def root() -> Dict[str, Any]:
    # await foo()  # you can add here a function and it will run in asynс
    return std_response(status='I\'m a teapot', info={"It's": "working"})


@app.get('/api/v1/tasks')
async def tasks_list() -> Dict[str, Any]:
    return std_response(status='OK', info=db)


@app.post('/api/v1/tasks')
async def add_task(task: Task) -> Dict[str, Any]:
    # expect in json body all fields from models.Task and interprets like new Task object
    db.append(task)
    return std_response(status='OK', info={"id": task.id})


@app.get('/api/v1/tasks/{task_id}/')
async def get_task(task_id: str) -> Dict[str, Any]:
    for task in db:
        if str(task.id) == str(task_id):
            return std_response(status='OK', info={"id": task.id, "question": task.question, "answer": task.answer})
    raise HTTPException(status_code=404, detail=f'Task {task_id} does not exist')


@app.put('/api/v1/tasks/{task_id}/')
async def update_task(task_update: TaskUpdateRequest, task_id: str) -> Dict[str, Any]:
    for task in db:
        if str(task.id) == str(task_id):
            if task_update.question:
                task.question = task_update.question
            if task_update.answer:
                task.answer = task_update.answer
            return std_response(status='OK', info={"id": task.id})
    raise HTTPException(status_code=404, detail=f'Task {task_id} does not exist')


@app.delete('/api/v1/tasks/{task_id}/')
async def delete_task(task_id: UUID) -> Dict[str, Any]:
    for task in db:
        if str(task.id) == str(task_id):
            db.remove(task)
            return std_response(status='OK', info={"id": task.id})
    raise HTTPException(status_code=404, detail=f'Task {task_id} does not exist')


# TODO: Add endpoints for checking answers (use id of task in url and check the text from answer, handle types of tasks)
@app.get('/api/v1/tasks/check/{task_id}/')
async def check_the_answer(task_id: UUID) -> Dict[str, Any]:

    # check type

    # check answer

    return std_response(status='OK', info={"id": task_id})



@app.get('/hello/{name}')  # test atribute from url
async def root(name: str) -> Dict[str, str]:
    return {"Hi": name}

