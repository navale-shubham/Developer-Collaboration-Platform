from sqlmodel import SQLModel, Field


class TeamInvitation(SQLModel, table=True):
    team_id: int = Field(primary_key=True)
    invited_user_id: int = Field(primary_key=True)
    inviter_user_id: int = Field(primary_key=True)