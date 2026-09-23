from fastapi import FastAPI

from app.schemas import *
from app.api.v1 import api


app = FastAPI()

app.include_router(
    api.app,
    prefix='/api'
)


@app.get("/")
def home():
    return {"message": "Welcome to Developer Collaboration Platform"}
