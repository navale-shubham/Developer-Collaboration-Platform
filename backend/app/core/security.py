import jwt
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash

from .config import SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRES_IN_MINUTES


password_hash = PasswordHash.recommended()


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