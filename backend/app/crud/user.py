from sqlmodel import select

from app.models import User

from .base import CRUDBase


class CRUDUser(CRUDBase):
    def create(self, name: str, username: str, password: str):
        user = User(
            name=name,
            username=username,
            password=password
        )

        self.db.add(user)
        return user

    def exists(self, username: str):
        return bool(
            self.db.exec(select(User).where(User.username == username)).first()
        )
    
    def get_from_id(self, id: int):
        return self.db.exec(select(User).where(User.id == id)).first()
    
    def get_from_username(self, username: str):
        return self.db.exec(select(User).where(User.username == username)).first()