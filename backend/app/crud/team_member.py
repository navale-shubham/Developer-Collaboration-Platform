from sqlmodel import select

from app.models import TeamMember

from .base import CRUDBase


class CRUDTeamMember(CRUDBase):
    def create(self, user_id: int, team_id: int):
        team_member = TeamMember(
            user_id=user_id,
            team_id=team_id
        )
        
        self.db.add(team_member)
        return team_member
    
    def get_all_team_ids(self, user_id: int):
        return self.db.exec(
            select(TeamMember.team_id).where(TeamMember.user_id == user_id)
        ).all()
    
    def exists(self, user_id: int, team_id: int):
        return bool(self.db.exec(select(TeamMember).where(
                TeamMember.user_id == user_id,
                TeamMember.team_id == team_id
        )).first()
        )
    
    def get_all_user_ids(self, team_id: int):
        return self.db.exec(select(TeamMember.user_id).where(TeamMember.team_id == team_id)).all()