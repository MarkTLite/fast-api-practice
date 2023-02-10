from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_access_token(name: str = '', password: str = ''):
    """Helper to get access_token"""
    response = client.post(
        "/token",
        data={
            "username": name,
            "password": password,
        },
    )
    return response.json().get('access_token')

def test_get_all_blogs():
    """Test getting all blogs works well"""
    response = client.get("/blog/all")
    assert response.status_code == 200

def test_auth_error():
    response = client.post(
        "/token",
        data={
            "username": "",
            "password": "",
        },
    )
    access_token = response.json().get('access_token')
    assert access_token == None
    message = response.json().get('detail')[0].get('msg')
    assert message == 'field required'


def test_auth_success():
    access_token = get_access_token('cat', 'string')
    assert access_token

def test_post_article():
    token = get_access_token('cat', 'string')
    assert token
    response = client.post(
        '/article/create',
         json={
            'title': 'Test Article',
            'content': 'Article Content',
            'published': True,
            'creator_id': 1
         },
         headers={
            'Authorization': f'bearer {token}'
         }
    )
    assert response.status_code == 200
    assert response.json().get('title') == 'Test Article'
