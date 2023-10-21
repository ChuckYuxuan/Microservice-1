#
# FastAPI is a framework and library for implementing REST web services in Python.
# https://fastapi.tiangolo.com/
#
from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import RedirectResponse

from fastapi.staticfiles import StaticFiles
from typing import List, Union

import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {'message': 'Hello, World from FastAPI Microservice 1!'}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8011)

