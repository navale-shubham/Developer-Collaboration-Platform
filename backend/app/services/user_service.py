from app.core.database import session
from app.crud import CRUDUser


class UserExistsError(Exception):
    pass


@session
def register_new_user(session, name, username, password):
    user_repo = CRUDUser(session)

    if user_repo.exists(username):
        raise UserExistsError()
    
    user_repo.create(name, username, password)


@session
def get_user_by_username(session, username):
    user_repo = CRUDUser(session)
    return user_repo.get_from_username(username)