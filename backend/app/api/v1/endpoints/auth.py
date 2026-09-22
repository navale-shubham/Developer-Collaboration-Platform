from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app.core.config import TOKEN_URL
from app.models import User
from app.schemas import UserRegister, Token
from app.services.auth_service import (
    authenticate_user, verify_current_user, verify_team_membership,
    InvalidCredentialsError, UserNotVerifiedError, TeamNotFoundError
)
from app.services.user_service import register_new_user, UserExistsError


app = APIRouter(
    prefix='/auth',
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        return verify_current_user(token)
    
    except UserNotVerifiedError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={'WWW-Authenticate': 'Bearer'}
        )


def require_team_membership(team_slug: str, user: Annotated[User, Depends(get_current_user)]):
    try:
        return verify_team_membership(team_slug, user)
    
    except TeamNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found."
        )


@app.post(
    '/register',
    status_code=status.HTTP_201_CREATED
)
def register(user: UserRegister):
    try:
        register_new_user(user.name, user.username, user.password)
    
    except UserExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User with same email already exists.'
        )


@app.post(
    '/login',
    status_code=status.HTTP_200_OK,
    response_model=Token
)
def login(login_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        return authenticate_user(login_data.username, login_data.password)
    
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid username or password.'
        )