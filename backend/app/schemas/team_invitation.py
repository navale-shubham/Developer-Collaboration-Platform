from sqlmodel import SQLModel


class TeamInvitationResponse(SQLModel):
    invited_user: UserViewResponse
    inviter_user: UserViewResponse