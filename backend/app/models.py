from sqlmodel import SQLModel, Field
from pwdlib import PasswordHash


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    username: str = Field(unique=True)
    password: str

    def verify_password(self, password):
        return PasswordHash.recommended().verify(password, self.password)

class UserBase(SQLModel):
    username: str = Field(unique=True)
    password: str

class UserRegister(UserBase):
    name: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.password = PasswordHash.recommended().hash(self.password)

class UserLogin(UserBase):
    pass


class Token(SQLModel):
    access_token: str
    token_type: str
