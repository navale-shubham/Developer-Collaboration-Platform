import jwt
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.config import SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRES_IN_MINUTES
from app.crud.user import CRUDUser
from app.core.database import get_db
from app.schemas.user import UserBase, UserResponse


password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str):
    return password_hash.hash(password)


def verify_hashed_password(password: str, hashed_password: str):
    return password_hash.verify(password, hashed_password)


def create_access_token(sub: str):
    expiration = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN_MINUTES)

    payload = {
        'sub': sub,
        'exp': expiration
    }
    
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload['sub'], None
    
    except jwt.ExpiredSignatureError:
        return None, 'Error: The token has expired.'
    
    except jwt.InvalidTokenError:
        return None, 'Error: Invalid token signature or payload.'


def get_me(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_repo = CRUDUser(db)
    
    username, error = verify_access_token(token)

    if username and (user := user_repo.get(
        UserBase(username=username)
    )):
        return UserResponse(**user.model_dump(include={'username', 'name'}))
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=error,
        headers={'WWW-Authenticate': 'Bearer'}
    )