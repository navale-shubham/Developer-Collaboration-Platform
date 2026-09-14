from sqlmodel import Session, SQLModel, create_engine, select
from functools import wraps

from app.models import User

from app.config import DATABASE_URL


class DataBase:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
    
    @staticmethod
    def session(func):
        '''A decorator to automatically provide session object to functions.'''

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            with Session(self.engine) as session:
                return func(self, session, *args, **kwargs)
        
        return wrapper
    
    def init(self):
        '''Create structure of the database.'''

        SQLModel.metadata.create_all(self.engine)
    
    def close(self):
        self.engine.dispose()
    
    @session
    def create_user(self, session, user_data):
        '''Add a new user in the database.'''

        user = User(
            name=user_data.name,
            username=user_data.username,
            password=user_data.password
        )

        session.add(user)
        session.commit()

    @session
    def user_exists(self, session, user):
        '''Check if the user exists in the database.'''

        return bool(
            session.exec(select(User).where(User.username == user.username)).first()
        )
    
    @session
    def read_user(self, session, user):
        '''Return user if present in the database.'''

        return session.exec(select(User).where(User.username == user.username)).first()


database = DataBase()
