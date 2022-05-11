from typing import Dict, Any

from fastapi import FastAPI


app = FastAPI()  # initial web application
"""You can rung this application locally with terminal command:
        uvicorn src.main:app --reload
    Optional use --reload for debugging.
    
    Also you can work with app with Docker
    
"""

# Endpoint's system


@app.get('/')  # root endpoint
async def root() -> Dict[str, Any]:
    # await foo()  # you can add here a function and it will run in asynh
    return {"It's": "working"}











@app.get('/hello/{name}')  # test atribute from url
async def root(name: str) -> Dict[str, str]:
    return {"Hi": name}

