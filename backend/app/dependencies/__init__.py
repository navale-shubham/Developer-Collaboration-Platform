from typing import Annotated

from fastapi import Depends

from app.core.database import get_db
from app.models import User

from .auth import get_current_user
from .teams import require_team_membership


CurrentUser = Annotated[User, Depends(get_current_user)]
DBSession = Annotated['Session', Depends(get_db)]