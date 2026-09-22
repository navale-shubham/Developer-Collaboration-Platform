from sqlmodel import SQLModel


class UserBase(SQLModel):
    name: str
    username: str

    model_config = {"from_attributes": True}


class UserRegister(UserBase):
    password: str


class UserResponse(UserBase):
    pass


class UserViewResponse(UserBase):
    pass