from sqlmodel import Session, create_engine, SQLModel
from functools import wraps

from .config import DATABASE_URL


engine = create_engine(DATABASE_URL)


def init_db():
    SQLModel.metadata.create_all(engine)


def dispose_db():
    engine.dispose()


def session(func):
    @wraps(func)
    def session_wrapper(*args, **kwargs):
        with Session(engine, expire_on_commit=False) as session, session.begin():
            return func(session, *args, **kwargs)
    
    return session_wrapper