from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Depends

from app.services.user_service import get_user_by_username
from app.schemas import UserResponse, UserViewResponse
from app.models import User

from .auth import get_current_user


app = APIRouter(
    prefix='/users'
)


@app.get(
    '/me',
    status_code=status.HTTP_200_OK,
    response_model=UserResponse
)
def get_me(user: Annotated[User, Depends(get_current_user)]):
    return user


@app.get(
    '/{username}',
    status_code=status.HTTP_200_OK,
    response_model=UserViewResponse
)
def get_user(username: str):
    if not (user := get_user_by_username(username)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found.'
        )
    
    return user