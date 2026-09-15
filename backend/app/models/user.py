from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    username: str = Field(unique=True)
    password: str

    def hash_password(self):
        from app.core.security import hash_password
        self.password = hash_password(self.password)

    def verify_password(self, password):
        from app.core.security import verify_hashed_password
        return verify_hashed_password(password, self.password)
