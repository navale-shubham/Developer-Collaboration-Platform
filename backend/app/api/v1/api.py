from fastapi import APIRouter

from .endpoints import auth, user


app = APIRouter()

app.include_router(auth.app)
app.include_router(user.app)