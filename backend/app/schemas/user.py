from sqlmodel import SQLModel


class UserBase(SQLModel):
    username: str

class UserRegister(UserBase):
    name: str
    password: str

class UserLogin(UserBase):
    password: str

class UserResponse(UserBase):
    name: str