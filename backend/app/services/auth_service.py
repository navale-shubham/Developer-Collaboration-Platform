from app.core.database import session
from app.core.security import (
    create_access_token, verify_access_token,
    TokenVerificationError
)
from app.schemas import Token
from app.crud import CRUDUser, CRUDTeam, CRUDTeamMember


class InvalidCredentialsError(Exception):
    pass

class UserNotVerifiedError(Exception):
    pass

class TeamNotFoundError(Exception):
    pass


@session
def verify_current_user(session, token):
    try:
        username = verify_access_token(token)
        user_repo = CRUDUser(session)

        return user_repo.get_from_username(username)
    
    except TokenVerificationError:
        raise UserNotVerifiedError()


@session
def authenticate_user(session, username, password):
    user_repo = CRUDUser(session)
    user = user_repo.get_from_username(username)

    if not user or not user.verify_password(password):
        raise InvalidCredentialsError()
    
    return Token(
        access_token=create_access_token(username),
        token_type='bearer'
    )


@session
def verify_team_membership(session, team_slug, user):
    team_repo = CRUDTeam(session)
    team_member_repo = CRUDTeamMember(session)

    team = team_repo.get_from_slug(team_slug)

    if not team or not team_member_repo.exists(user.id, team.id):
        raise TeamNotFoundError()
    
    return team