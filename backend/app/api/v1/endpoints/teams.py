from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from app.dependencies import CurrentUser, DBSession, require_team_membership
from app.crud import CRUDTeam, CRUDUser, CRUDTeamMember, CRUDTeamInvitation
from app.schemas import TeamResponse, TeamInvitationResponse, UserViewResponse


app = APIRouter(
    prefix='/teams'
)


@app.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=list[TeamResponse]
)
def get_teams(user: CurrentUser, db: DBSession):
    team_member_repo = CRUDTeamMember(db)
    team_repo = CRUDTeam(db)

    team_ids = team_member_repo.get_all_team_ids(user.id)
    return [team_repo.get_from_id(team_id) for team_id in team_ids]


@app.post(
    '/',
    status_code=status.HTTP_201_CREATED
)
def create_team(
    team_name: str,
    user: CurrentUser,
    db: DBSession
):
    team_repo = CRUDTeam(db)
    team_member_repo = CRUDTeamMember(db)
    
    team = team_repo.create(team_name, user.id)
    db.commit()
    db.refresh(team)

    team_member_repo.create(user.id, team.id)


@app.get(
    '/{team_slug}',
    status_code=status.HTTP_200_OK,
    response_model=TeamResponse
)
def get_team(
    team: Annotated[Team, Depends(require_team_membership)]
):
    return team


@app.get(
    '/{team_slug}/invitations',
    status_code=status.HTTP_200_OK
)
def get_team_invitations(
    user: CurrentUser,
    db: DBSession,
    team: Annotated[Team, Depends(require_team_membership)]
):
    team_invitation_repo = CRUDTeamInvitation(db)
    user_repo = CRUDUser(db)

    team_invitations = team_invitation_repo.get_for_team(team.id)
    return [TeamInvitationResponse(
        invited_user=user_repo.get_from_id(team_invitation.invited_user_id),
        inviter_user=user_repo.get_from_id(team_invitation.inviter_user_id)
    ) for team_invitation in team_invitations]


@app.post(
    '/{team_slug}/invitations',
    status_code=status.HTTP_200_OK
)
def create_team_invitation(
    invited_user_username: str,
    user: CurrentUser,
    db: DBSession,
    team: Annotated[Team, Depends(require_team_membership)]
):
    team_invitation_repo = CRUDTeamInvitation(db)
    user_repo = CRUDUser(db)
    team_member_repo = CRUDTeamMember(db)

    invited_user = user_repo.get_from_username(invited_user_username)
    if not invited_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Invited user not found.'
        )
    
    if team_member_repo.exists(invited_user.id, team.id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Invited user is already part of same team.'
        )
    
    team_invitation_repo.create(
        team.id,
        invited_user.id,
        user.id
    )


@app.get(
    '/{team_slug}/members',
    status_code=status.HTTP_200_OK,
    response_model=list[UserViewResponse]
)
def get_team_memebers(
    db: DBSession,
    team: Annotated[Team, Depends(require_team_membership)]
):
    team_member_repo = CRUDTeamMember(db)
    user_repo = CRUDUser(db)

    user_ids = team_member_repo.get_all_user_ids(team.id)
    return [user_repo.get_from_id(user_id) for user_id in user_ids]


@app.post(
    '/{team_slug}/members',
    status_code=status.HTTP_200_OK
)
def add_team_member(
    team_slug: str,
    user: CurrentUser,
    db: DBSession
):
    team_repo = CRUDTeam(db)
    team_invitation_repo = CRUDTeamInvitation(db)
    team_member_repo = CRUDTeamMember(db)

    team = team_repo.get_from_slug(team_slug)

    if not team_invitation_repo.exists(team.id, user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Invitation not found.'
        )
    
    team_member_repo.create(user.id, team.id)
    team_invitation_repo.delete(team.id, user.id)

    team.inc_size()
    db.add(team)