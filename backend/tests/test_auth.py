def test_register(client):
    user = {
        'name': 'shubham',
        'username': 'user_shubham',
        'password': '123456'
    }

    response = client.post(
        '/auth/register',
        json=user
    )

    assert response.status_code == 201

def test_register_conflict(client):
    user = {
        'name': 'shubham',
        'username': 'user_shubham',
        'password': '123456'
    }

    response = client.post(
        '/auth/register',
        json=user
    )

    assert response.status_code == 409


def test_login(client):
    user = {
        'username': 'user_shubham',
        'password': '123456'
    }

    response = client.post(
        '/auth/login',
        data=user
    )

    assert response.status_code == 200


def test_login_invalid_username(client):
    user = {
        'username': 'user_invalid',
        'password': '000000'
    }

    response = client.post(
        '/auth/login',
        data=user
    )

    assert response.status_code == 403


def test_login_invalid_password(client):
    user = {
        'username': 'user_shubham',
        'password': 'password_invalid'
    }

    response = client.post(
        '/auth/login',
        data=user
    )

    assert response.status_code == 403


def test_token_authentication(client):
    user = {
        'username': 'user_shubham',
        'password': '123456'
    }

    response = client.post(
        '/auth/login',
        data=user
    )

    data = response.json()
    token = data.get('access_token')
    ttype = data.get('token_type')

    response = client.get(
        '/users/me',
        headers = {
            'Authorization': f'{ttype} {token}'
        }
    )

    assert response.status_code == 200


def test_fake_token_authentication(client):
    response = client.get(
        '/users/me',
        headers = {
            'Authorization': f'Bearer fake-token'
        }
    )

    assert response.status_code == 401
