from fastapi import APIRouter

from .endpoints import auth, users, teams


app = APIRouter(
    prefix='/v1'
)

app.include_router(auth.app)
app.include_router(users.app)
app.include_router(teams.app)