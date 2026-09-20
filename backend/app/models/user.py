from sqlmodel import SQLModel, Field, Relationship

from app.core.security import hash_password, verify_hashed_password


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    username: str = Field(unique=True)
    password: str

    teams: list[Team] = Relationship(back_populates='owner')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.hash_password()

    def hash_password(self):
        self.password = hash_password(self.password)

    def verify_password(self, password):
        return verify_hashed_password(password, self.password)