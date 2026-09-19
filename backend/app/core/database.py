from sqlmodel import Session, create_engine

from .config import DATABASE_URL


engine = create_engine(DATABASE_URL)

def get_db():
    with Session(engine) as db:
        yield db
        db.commit()