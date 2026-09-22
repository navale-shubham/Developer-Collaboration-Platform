from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from app.schemas import TeamResponse, TeamInvitationResponse, UserViewResponse
from app.models import User, Team
from app.services.team_service import (
    fetch_teams_of_user, create_new_team, fetch_team_invitations,
    create_new_team_invitation, fetch_team_members, add_new_team_member,
    UserNotFoundError, UserExistsInTeamError, InvitationNotFoundError
)

from .auth import get_current_user, require_team_membership


app = APIRouter(
    prefix='/teams'
)


@app.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=list[TeamResponse]
)
def get_teams(user: Annotated[User, Depends(get_current_user)]):
    return fetch_teams_of_user(user)


@app.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=TeamResponse
)
def create_team(team_name: str, user: Annotated[User, Depends(get_current_user)]):
    return create_new_team(user, team_name)


@app.get(
    '/{team_slug}',
    status_code=status.HTTP_200_OK,
    response_model=TeamResponse
)
def get_team(team: Annotated[Team, Depends(require_team_membership)]):
    return team


@app.get(
    '/{team_slug}/invitations',
    status_code=status.HTTP_200_OK,
    response_model=list[TeamInvitationResponse]
)
def get_team_invitations(
    user: Annotated[User, Depends(get_current_user)],
    team: Annotated[Team, Depends(require_team_membership)]
):
    return fetch_team_invitations(user, team)


@app.post(
    '/{team_slug}/invitations',
    status_code=status.HTTP_200_OK,
    response_model=TeamInvitationResponse
)
def create_team_invitation(
    invited_user_username: str,
    user: Annotated[User, Depends(get_current_user)],
    team: Annotated[Team, Depends(require_team_membership)]
):
    try:
        return create_new_team_invitation(user, team, invited_user_username)
    
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Invited user not found.'
        )
    
    except UserExistsInTeamError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Invited user is already part of same team.'
        )


@app.get(
    '/{team_slug}/members',
    status_code=status.HTTP_200_OK,
    response_model=list[UserViewResponse]
)
def get_team_memebers(team: Annotated[Team, Depends(require_team_membership)]):
    return fetch_team_members(team)


@app.post(
    '/{team_slug}/members',
    status_code=status.HTTP_200_OK,
    response_model=TeamResponse
)
def add_team_member(
    team_slug: str,
    user: Annotated[User, Depends(get_current_user)]
):
    try:
        return add_new_team_member(user, team_slug)
    
    except InvitationNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Invitation not found.'
        )