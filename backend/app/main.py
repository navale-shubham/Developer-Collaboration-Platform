from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from contextlib import asynccontextmanager
from typing import Annotated

from app.database import database
from app.models import UserRegister, UserLogin, User, Token
from app.security import create_access_token, verify_access_token


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.init()

    yield

    database.close()


app = FastAPI(lifespan=lifespan)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_me(token: str = Depends(oauth2_scheme)):
    username, error = verify_access_token(token)

    if username and database.user_exists(
        UserLogin(username=username, password='')
    ):
        return username
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=error,
        headers={'WWW-Authenticate': 'Bearer'}
    )


@app.get("/")
def home():
    return {"message": "Welcome to Developer Collaboration Platform"}


@app.post('/register', status_code=status.HTTP_201_CREATED)
def register(user: UserRegister):
    if database.user_exists(user):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={'message': 'User with same email already exists.'}
        )
    
    database.create_user(user)
    return 'User registration successful.'


@app.post('/login', status_code=status.HTTP_200_OK)
def login(login_data: OAuth2PasswordRequestForm = Depends()):
    user = database.read_user(login_data)

    if user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={'message': 'User not found.'}
        )
    
    if not user.verify_password(login_data.password):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={'message': 'Wrong password.'}
        )
    
    access_token = create_access_token(user.username)
    return Token(access_token=access_token, token_type="bearer")


@app.get('/users/me', status_code=status.HTTP_200_OK)
def me(username: str = Depends(get_me)):
    return username
