from tests.constants import URL, user_shubham, team_byteme, Headers


def test_team_creation(client, user):
    token_type, access_token = user(client, user_shubham)
    headers = Headers(token_type=token_type, access_token=access_token)()
    
    response = client.post(
        URL.teams,
        params={'team_name': team_byteme.name},
        headers=headers
    )

    assert response.status_code == 201

    team_data = response.json()

    response = client.get(
        URL.teams_lookup(team_data.get('slug')),
        headers=headers
    )

    assert response.status_code == 200
    assert response.json() == team_data

    response = client.get(
        URL.teams,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json() == [team_data]