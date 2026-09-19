from fastapi import FastAPI
from sqlmodel import SQLModel
from contextlib import asynccontextmanager

from app.models import *
from app.schemas import *

from app.core.database import engine
from app.api.v1 import api


UserResponse.model_rebuild()
TeamResponse.model_rebuild()
TeamInvitationResponse.model_rebuild()


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    
    yield

    engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(
    api.app,
    prefix='/api'
)


@app.get("/")
def home():
    return {"message": "Welcome to Developer Collaboration Platform"}
