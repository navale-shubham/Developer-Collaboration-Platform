from app.core.database import session
from app.crud import CRUDUser, CRUDTeam, CRUDTeamMember, CRUDTeamInvitation
from app.schemas import TeamInvitationResponse


class UserNotFoundError(Exception):
    pass

class UserExistsInTeamError(Exception):
    pass

class InvitationNotFoundError(Exception):
    pass


@session
def fetch_teams_of_user(session, user):
    team_member_repo = CRUDTeamMember(session)
    team_repo = CRUDTeam(session)

    team_ids = team_member_repo.get_all_team_ids(user.id)
    return [team_repo.get_from_id(team_id) for team_id in team_ids]


@session
def create_new_team(session, user, team_name):
    team_repo = CRUDTeam(session)
    team_member_repo = CRUDTeamMember(session)

    team = team_repo.create(team_name, user.id)

    session.flush()
    session.refresh(team)

    team_member_repo.create(user.id, team.id)

    return team


@session
def fetch_team_invitations(session, user, team):
    team_invitation_repo = CRUDTeamInvitation(session)
    user_repo = CRUDUser(session)

    team_invitations = team_invitation_repo.get_for_team(team.id)

    return [TeamInvitationResponse(
        invited_user=user_repo.get_from_id(team_invitation.invited_user_id),
        inviter_user=user_repo.get_from_id(team_invitation.inviter_user_id)
    ) for team_invitation in team_invitations]


@session
def create_new_team_invitation(session, user, team, invited_user_username):
    team_invitation_repo = CRUDTeamInvitation(session)
    user_repo = CRUDUser(session)
    team_member_repo = CRUDTeamMember(session)

    invited_user = user_repo.get_from_username(invited_user_username)
    if not invited_user:
        raise UserNotFoundError()
    
    if team_member_repo.exists(invited_user.id, team.id):
        raise UserExistsInTeamError()
    
    team_invitation = team_invitation_repo.create(
        team.id,
        invited_user.id,
        user.id
    )

    session.flush()
    session.refresh(team_invitation)

    return TeamInvitationResponse(
        invited_user=user_repo.get_from_id(team_invitation.invited_user_id),
        inviter_user=user_repo.get_from_id(team_invitation.inviter_user_id)
    )


@session
def fetch_team_members(session, team):
    team_member_repo = CRUDTeamMember(session)
    user_repo = CRUDUser(session)

    user_ids = team_member_repo.get_all_user_ids(team.id)

    return [user_repo.get_from_id(user_id) for user_id in user_ids]


@session
def add_new_team_member(session, user, team_slug):
    team_repo = CRUDTeam(session)
    team_invitation_repo = CRUDTeamInvitation(session)
    team_member_repo = CRUDTeamMember(session)

    team = team_repo.get_from_slug(team_slug)

    if not team_invitation_repo.exists(team.id, user.id):
        raise InvitationNotFoundError()
    
    team_member_repo.create(user.id, team.id)
    team_invitation_repo.delete(team.id, user.id)

    team.inc_size()
    
    session.add(team)
    session.flush()
    session.refresh(team)

    return team