from tests.constants import URL, user_shubham, user_pawan, team_byteme, Headers


def test_team_invitation_lifecycle(client, user):
    user_shubham_auth = user(client, user_shubham)
    user_pawan_auth = user(client, user_pawan)

    user_shubham_headers = Headers(token_type=user_shubham_auth[0], access_token=user_shubham_auth[1])()
    user_pawan_headers = Headers(token_type=user_pawan_auth[0], access_token=user_pawan_auth[1])()

    response = client.post(
        URL.teams,
        params={'team_name': team_byteme.name},
        headers=user_shubham_headers
    )

    if response.status_code != 201:
        raise Exception('Error in team creation.')
    
    response_data = response.json()
    team_slug = response_data.get('slug')

    response = client.post(
        URL.teams_invitations(team_slug),
        params={'invited_user_username': user_pawan.username},
        headers=user_shubham_headers
    )

    assert response.status_code == 200
    assert response.json() == {
          'invited_user': user_pawan.get_lookup_data(),
          'inviter_user': user_shubham.get_lookup_data()
        }
    
    response = client.get(
        URL.teams_invitations(team_slug),
        headers=user_shubham_headers
    )

    assert response.status_code == 200
    assert response.json() == [{
        'invited_user': user_pawan.get_lookup_data(),
        'inviter_user': user_shubham.get_lookup_data()
    }]

    response = client.post(
        URL.teams_members(team_slug),
        headers=user_pawan_headers
    )

    response_data = response.json()

    assert response.status_code == 200
    assert response_data['name'] == team_byteme.name
    assert response_data['size'] == 2
    assert response_data['owner'] == user_shubham.get_lookup_data()

    response = client.get(
        URL.teams_members(team_slug),
        headers=user_shubham_headers
    )

    assert response.status_code == 200
    assert response.json() == [
        user_shubham.get_lookup_data(),
        user_pawan.get_lookup_data()
    ]