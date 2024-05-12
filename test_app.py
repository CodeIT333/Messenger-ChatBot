import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_verify(client):
    response = client.get('/?hub.mode=subscribe&hub.challenge=7556135334443385&hub.verify_token=chatbot')
    assert response.status_code == 200
    assert response.data == b'7556135334443385'

def test_verify_token_mismatch(client):
    response = client.get('/?hub.mode=subscribe&hub.challenge=123&hub.verify_token=invalid_token')
    assert response.status_code == 403
    assert b'Verification token mismatch' in response.data

def test_webhook_post(client):
    response = client.post('/', json={
        "object": "page",
        "entry": [
            {
                "messaging": [
                    {
                        "sender": {"id": "7556135334443385"},
                        "message": {"text": "Hello"}
                    }
                ]
            }
        ]
    })
    assert response.status_code == 200
    assert response.data == b'ok'

def test_fetch_weather(client):
    response = client.post('/', json={
        "object": "page",
        "entry": [
            {
                "messaging": [
                    {
                        "sender": {"id": "7556135334443385"},
                        "message": {"text": "weather now"}
                    }
                ]
            }
        ]
    })
    assert response.status_code == 200
    assert b"ok" in response.data

def test_fetch_cinema(client):
    response = client.post('/', json={
        "object": "page",
        "entry": [
            {
                "messaging": [
                    {
                        "sender": {"id": "7556135334443385"},
                        "message": {"text": "movie movies"}
                    }
                ]
            }
        ]
    })
    assert response.status_code == 200
    assert b"ok" in response.data

def test_get_weather_for_the_next_10_days(client):
    response = client.post('/', json={
        "object": "page",
        "entry": [
            {
                "messaging": [
                    {
                        "sender": {"id": "7556135334443385"},
                        "message": {"text": "weather next days"}
                    }
                ]
            }
        ]
    })
    assert response.status_code == 200
    assert b"ok" in response.data
def test_help_command(client):
    response = client.post('/', json={
        "object": "page",
        "entry": [
            {
                "messaging": [
                    {
                        "sender": {"id": "7556135334443385"},
                        "message": {"text": "help"}
                    }
                ]
            }
        ]
    })
    assert response.status_code == 200
    assert b"ok" in response.data