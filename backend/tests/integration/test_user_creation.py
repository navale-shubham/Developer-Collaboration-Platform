from tests.constants import URL, user_shubham


def test_user_creation(client):
    response = client.post(
        URL.register,
        json=user_shubham.get_register_data()
    )

    assert response.status_code == 201

    response = client.post(
        URL.login,
        data=user_shubham.get_login_data()
    )

    assert response.status_code == 200

    data = response.json()
    token_type = data.get('token_type')
    access_token = data.get('access_token')

    response = client.get(
        URL.users_me,
        headers={"Authorization": f"{token_type} {access_token}"}
    )

    assert response.status_code == 200


def test_duplicate_user_creation(client, user):
    token_type, access_token = user(client, user_shubham)

    response = client.post(
        URL.register,
        json=user_shubham.get_register_data()
    )

    assert response.status_code == 409


def test_fake_user_login(client):
    response = client.post(
        URL.login,
        data=user_shubham.get_login_data()
    )

    assert response.status_code == 403


def test_fake_user_token_auth(client):
    response = client.get(
        URL.users_me,
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 401


def test_user_lookup_by_username(client, user):
    token_type, access_token = user(client, user_shubham)

    response = client.get(URL.users_lookup(user_shubham.username))

    assert response.status_code == 200
    assert response.json() == user_shubham.get_lookup_data()


def test_invalid_user_lookup_by_username(client):
    response = client.get(URL.users_lookup(user_shubham.username))

    assert response.status_code == 404