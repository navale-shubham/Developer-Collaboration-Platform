from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas import UserRegister, Token
from app.crud import CRUDUser
from app.core.security import create_access_token
from app.dependencies import DBSession


app = APIRouter(
    prefix='/auth',
)


@app.post('/register', status_code=status.HTTP_201_CREATED)
def register(user: UserRegister, db: DBSession):
    user_repo = CRUDUser(db)

    if user_repo.exists(user.username):
        raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail='User with same email already exists.'
    )
    
    user_repo.create(user.name, user.username, user.password)


@app.post('/login', status_code=status.HTTP_200_OK)
def login(
    login_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: DBSession
):
    user_repo = CRUDUser(db)
    user = user_repo.get_from_username(login_data.username)

    if user and user.verify_password(login_data.password):
        access_token = create_access_token(user.username)
        return Token(access_token=access_token, token_type="bearer")
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Invalid username or password.'
    )