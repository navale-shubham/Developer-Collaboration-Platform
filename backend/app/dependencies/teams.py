from typing import Annotated

from fastapi import Depends

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.crud import CRUDTeam, CRUDTeamMember
from app.models import User


def require_team_membership(
    team_slug: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    team_repo = CRUDTeam(db)
    team_member_repo = CRUDTeamMember(db)

    team = team_repo.get_from_slug(team_slug)

    if team and team_member_repo.exists(user.id, team.id):
        return team

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Team not found.",
    )