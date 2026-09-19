from fastapi import APIRouter, status, HTTPException

from app.dependencies import CurrentUser, DBSession
from app.schemas import UserResponse, UserViewResponse
from app.crud import CRUDUser


app = APIRouter(
    prefix='/users'
)


@app.get(
    '/me',
    status_code=status.HTTP_200_OK,
    response_model=UserResponse
)
def get_me(user: CurrentUser):
    return user


@app.get(
    '/{username}',
    status_code=status.HTTP_200_OK,
    response_model=UserViewResponse
)
def get_user(username: str, db: DBSession):
    user_repo = CRUDUser(db)

    user = user_repo.get_from_username(username)
    if user:
        return user
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='User not found.'
    )