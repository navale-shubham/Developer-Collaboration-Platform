from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.schemas.user import UserRegister, UserLogin
from app.schemas.token import Token
from app.crud.user import CRUDUser
from app.core.database import get_db
from app.core.security import create_access_token


app = APIRouter(
    prefix='/auth',
)


@app.post('/register', status_code=status.HTTP_201_CREATED)
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    user_repo = CRUDUser(db)

    if user_repo.exists(user):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={'message': 'User with same email already exists.'}
        )
    
    user_repo.create(user)


@app.post('/login', status_code=status.HTTP_200_OK)
def login(
    login_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user_repo = CRUDUser(db)

    user_login = UserLogin(
        username=login_data.username,
        password=login_data.password
    )

    user = user_repo.get(user_login)

    if user and user.verify_password(user_login.password):
        access_token = create_access_token(user.username)
        return Token(access_token=access_token, token_type="bearer")
    
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={'message': 'Invalid username or password.'}
    )