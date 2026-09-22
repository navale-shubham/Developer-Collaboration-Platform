from sqlmodel import select

from app.models import Team

from .base import CRUDBase


class CRUDTeam(CRUDBase):
    def create(self, name: str, owner_id: int):
        team = Team(
            name=name,
            owner_id=owner_id
        )
        
        self.db.add(team)
        return team
    
    def get_from_id(self, id: int):
        return self.db.exec(
            select(Team).where(Team.id == id)
        ).first()
    
    def get_from_slug(self, slug: str):
        return self.db.exec(
            select(Team).where(Team.slug == slug)
        ).first()