from sqlmodel import SQLModel


class TeamResponse(SQLModel):
    name: str
    slug: str
    size: int
    owner: UserViewResponse

    model_config = {"from_attributes": True}