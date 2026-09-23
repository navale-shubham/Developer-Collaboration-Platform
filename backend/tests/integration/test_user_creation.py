from tests.constants import (
    URL_REGISTER, URL_LOGIN, URL_USERS_ME, URL_USERS, TEST_USERNAME, TEST_NAME,
    TEST_USER_REGISTER_DATA, TEST_USER_LOGIN_DATA, TEST_FAKE_USER_LOGIN_DATA
)

def test_user_creation(client):
    response = client.post(
        URL_REGISTER,
        json=TEST_USER_REGISTER_DATA
    )

    assert response.status_code == 201

    response = client.post(
        URL_LOGIN,
        data=TEST_USER_LOGIN_DATA
    )

    assert response.status_code == 200

    data = response.json()
    access_token = data.get('access_token')
    token_type = data.get('token_type')

    response = client.get(
        URL_USERS_ME,
        headers={"Authorization": f"{token_type} {access_token}"}
    )

    assert response.status_code == 200


def test_duplicate_user_creation(client):
    response = client.post(
        URL_REGISTER,
        json=TEST_USER_REGISTER_DATA
    )

    assert response.status_code == 409


def test_fake_user_login(client):
    response = client.post(
        URL_LOGIN,
        data=TEST_FAKE_USER_LOGIN_DATA
    )

    assert response.status_code == 403


def test_fake_user_token_auth(client):
    response = client.get(
        URL_USERS_ME,
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 401


def test_user_lookup_by_username(client):
    response = client.get(
        f'{URL_USERS}/{TEST_USERNAME}',
    )

    assert response.status_code == 200
    assert response.json() == {
        'name': TEST_NAME,
        'username': TEST_USERNAME
    }


def test_invalid_user_lookup_by_username(client):
    response = client.get(
        f'{URL_USERS}/fake_username',
    )

    assert response.status_code == 404