from dataclasses import dataclass, asdict


class URL:
    BASE = '/api/v1'

    register = BASE + '/auth/register'
    login = BASE + '/auth/login'
    users = BASE + '/users'
    users_me = users + '/me'
    users_lookup = lambda username: URL.users + f'/{username}'
    teams = BASE + '/teams'
    teams_lookup = lambda team_slug: URL.teams + f'/{team_slug}'
    teams_invitations = lambda team_slug: URL.teams + f'/{team_slug}' + '/invitations'
    teams_members = lambda team_slug: URL.teams + f'/{team_slug}' + '/members'


@dataclass
class User:
    name: str
    username: str
    password: str

    def get_lookup_data(self):
        return {
            'name': self.name,
            'username': self.username
        }

    def get_register_data(self):
        return asdict(self)
    
    def get_login_data(self):
        return {
            'username': self.username,
            'password': self.password
        }


@dataclass
class Team:
    name: str


@dataclass
class Headers:
    token_type: str = None
    access_token: str = None

    def __call__(self, authorization=True):
        headers = {}

        if authorization and self.token_type and self.access_token:
            headers['Authorization'] = f'{self.token_type} {self.access_token}'
        
        return headers


user_shubham = User(name='Shubham Navale', username='shubham', password='000000')
user_pawan = User(name='Pawan Nikam', username='pawan', password='111111')

team_byteme = Team(name='ByteMe')
