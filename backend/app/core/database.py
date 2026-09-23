from sqlmodel import Session, create_engine, SQLModel
from functools import wraps

from .config import DATABASE_URL


engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)


def session(func):
    @wraps(func)
    def session_wrapper(*args, **kwargs):
        with Session(engine, expire_on_commit=False) as session, session.begin():
            return func(session, *args, **kwargs)
    
    return session_wrapper