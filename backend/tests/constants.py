URL_BASE = '/api/v1'
URL_REGISTER = URL_BASE + '/auth/register'
URL_LOGIN = URL_BASE + '/auth/login'
URL_USERS = URL_BASE + '/users'
URL_USERS_ME = URL_USERS + '/me'
URL_TEAMS = URL_BASE + '/teams'
URL_TEAMS_INVITATIONS = lambda team_slug: URL_TEAMS + f'/{team_slug}' + '/invitations'
URL_TEAMS_MEMBERS = lambda team_slug: URL_TEAMS + f'/{team_slug}' + '/members'

TEST_NAME = 'Shubham Navale'
TEST_USERNAME = 'shub'
TEST_PASSWORD = '123456'

TEST_USER_REGISTER_DATA = {
    'name': TEST_NAME,
    'username': TEST_USERNAME,
    'password': TEST_PASSWORD
}

TEST_USER_LOGIN_DATA = {
    'username': TEST_USERNAME,
    'password': TEST_PASSWORD
}

TEST_FAKE_USER_LOGIN_DATA = {
    'username': 'fake_username',
    'password': 'fake_password'
}