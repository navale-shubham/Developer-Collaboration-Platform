from fastapi import APIRouter, Depends, status

from app.core.security import get_me
from app.schemas.user import UserResponse


app = APIRouter(
    prefix='/users'
)

@app.get('/me', status_code=status.HTTP_200_OK)
def me(user: UserResponse = Depends(get_me)):
    return user
