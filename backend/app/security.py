import jwt
from datetime import datetime, timedelta, timezone

from app.config import SECRET_KEY, JWT_ALGORITHM


def create_access_token(username: str, expires_in_minutes: int = 30):
    expiration = datetime.now(timezone.utc) + timedelta(minutes=expires_in_minutes)

    payload = {
        'sub': username,
        'exp': expiration
    }
    
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload['sub'], None
    
    except jwt.ExpiredSignatureError:
        return None, 'Error: The token has expired.'
    
    except jwt.InvalidTokenError:
        return None, 'Error: Invalid token signature or payload.'
