from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.core.config import TOKEN_URL
from app.core.database import get_db
from app.core.security import verify_access_token
from app.crud import CRUDUser


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated['Session', Depends(get_db)]
):
    user_repo = CRUDUser(db)
    
    username, error = verify_access_token(token)

    if username and (user := user_repo.get_from_username(username)):
        return user
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=error,
        headers={'WWW-Authenticate': 'Bearer'}
    )