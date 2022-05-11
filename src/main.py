from typing import Dict, Any, List
from uuid import uuid4

from fastapi import FastAPI

from src.constants import STATUSES
from src.models import Task, TaskType
from src.utils import std_response

app = FastAPI()  # initial web application
"""You can rung this application locally with terminal command:
        uvicorn src.main:app --reload
    Optional use --reload for debugging.
    
    Also you can work with app with Docker
    
"""

#fake database with fake task
db: List[Task] = [
    Task(id="691ce00a-490e-4c9c-938e-76f9044a8af4", type=TaskType.russian_to_english, russian='Привет', english=['Hi', 'Hello']),
    Task(id="2cf66c85-43bb-4553-94e4-583e9790a60f", type=TaskType.english_to_russian, russian=['Привет', 'Здравствуйте'], english='Hi'),
]

# Endpoint's system


@app.get('/')  # root endpoint
async def root() -> Dict[str, Any]:
    # await foo()  # you can add here a function and it will run in asynс
    return std_response(status=STATUSES.get('I\'m a teapot'), info={"It's": "working"})


@app.get('/api/v1/tasks/')
async def tasks_list() -> Dict[str, Any]:
    return std_response(status=STATUSES.get('OK'), info=db)


@app.post('/api/v1/tasks/')
async def add_task(task: Task) -> Dict[str, Any]:
    # expect in json body all fields from models.Task and interprets like new Task object
    db.append(task)
    return std_response(status=STATUSES.get('OK'), info={"id": task.id})








@app.get('/hello/{name}')  # test atribute from url
async def root(name: str) -> Dict[str, str]:
    return {"Hi": name}

