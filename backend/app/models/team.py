from sqlmodel import SQLModel, Field, Relationship

from app.core.utils import generate_slug


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    slug: str | None = Field(default=None, unique=True)
    size: int | None = Field(default=1)
    owner_id: int = Field(foreign_key='user.id')

    owner: User = Relationship(back_populates='teams', sa_relationship_kwargs={"lazy": "selectin"})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.slug = generate_slug(self.name)
    
    def inc_size(self):
        self.size += 1