from sqlmodel import select

from app.schemas.user import UserBase, UserRegister
from app.models.user import User
from app.crud.base import CRUDBase


class CRUDUser(CRUDBase):
    def create(self, user: UserRegister):
        user = User(**user.model_dump())
        user.hash_password()
        self.db.add(user)

    def exists(self, user: UserBase):
        return bool(
            self.db.exec(select(User).where(User.username == user.username)).first()
        )
    
    def get(self, user: UserBase):
        return self.db.exec(select(User).where(User.username == user.username)).first()