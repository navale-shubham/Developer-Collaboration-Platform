from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.schemas import *
from app.core.database import dispose_db, init_db
from app.api.v1 import api


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    dispose_db()


app = FastAPI(lifespan=lifespan)
app.include_router(
    api.app,
    prefix='/api'
)


@app.get("/")
def home():
    return {"message": "Welcome to Developer Collaboration Platform"}
