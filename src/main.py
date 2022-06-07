from typing import Dict, Any

from fastapi import FastAPI, Request
from pydantic import ValidationError

from src.basecore.std_response import Response
from src.task.router import router as task_router
from src.user.router import router as user_router


app = FastAPI()  # initial web application
"""
    You can rung this application locally with terminal command:
        uvicorn src.main:app --reload
    Optional use --reload for debugging.  
    Also you can work with app with Docker containers
    make start
"""


# Endpoint's system
@app.get('/')  # root endpoint
async def root() -> Dict[str, Any]:
    # await foo()  # you can add here a function and it will run in asynс
    return {"status": 418, "info": "It's working"}

app.include_router(router=task_router, prefix='/task', tags=['task'])
app.include_router(router=user_router, prefix='/user', tags=['user'])

# TODO: Add error handler
