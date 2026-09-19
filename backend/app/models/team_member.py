from sqlmodel import SQLModel, Field


class TeamMember(SQLModel, table=True):
    user_id: int = Field(foreign_key='user.id', primary_key=True)
    team_id: int = Field(foreign_key='team.id', primary_key=True)