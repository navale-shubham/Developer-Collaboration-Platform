from sqlmodel import select, delete

from app.models import TeamInvitation

from .base import CRUDBase


class CRUDTeamInvitation(CRUDBase):
    def create(self, team_id, invited_user_id, inviter_user_id):
        self.db.add(TeamInvitation(
            team_id=team_id,
            invited_user_id=invited_user_id,
            inviter_user_id=inviter_user_id
        ))
    
    def delete(self, team_id, invited_user_id):
        self.db.exec(
            delete(TeamInvitation).where(
                TeamInvitation.team_id == team_id,
                TeamInvitation.invited_user_id == invited_user_id
            )
        )
    
    def exists(self, team_id, invited_user_id):
        return bool(
            self.db.exec(
                select(TeamInvitation).where(
                    TeamInvitation.team_id == team_id,
                    TeamInvitation.invited_user_id == invited_user_id
                )
            )
        )
    
    def get_for_invited_user(self, invited_user_id: int):
        return self.db.exec(
            select(TeamInvitation).where(TeamInvitation.invited_user_id == invited_user_id)
        ).all()
    
    def get_for_team(self, team_id: int):
        return self.db.exec(
            select(TeamInvitation).where(TeamInvitation.team_id == team_id)
        ).all()