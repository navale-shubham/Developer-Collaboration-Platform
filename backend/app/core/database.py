from sqlmodel import Session, create_engine, SQLModel

from .config import DATABASE_URL


engine = create_engine(DATABASE_URL)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as db:
        yield db
        db.commit()


def dispose_db():
    engine.dispose()