import json
import requests
SERVER_URL = 'http://localhost:5000/'


def test_register():
    data = {
        "username": "testUser20",
        "password": "123456"
    }
    response = requests.post(SERVER_URL + 'register', json=data)
    assert response.status_code == 201

def test_login():
    data = {
        "username": "testUser10",
        "password": "123456"
    }
    response = requests.post(SERVER_URL + 'login', json=data)
    assert response.status_code == 200
    assert 'token' in response.json()
    access_token = response.json()['token']
    assert access_token is not None
    headers = {"Authorization": access_token}
    test_login.headers = headers

def test_add_movie_to_list():
    data = {
        "title": "Test Movie",
        "genre": "Action"
    }
    response = requests.post(SERVER_URL + 'add_movie', json=data, headers=test_login.headers)
    assert response.status_code == 201

def test_get_user_movies():
    response = requests.get(SERVER_URL + 'movies', headers=test_login.headers)
    assert response.status_code == 200
    assert isinstance(response.json().get('movies'), list)

def test_add_movies_from_api():
    response = requests.post(SERVER_URL + 'populate_movies')
    assert response.status_code == 200

def test_update_rating():
    data = {
        "movie_id": 1,
        "rating": 8
    }
    response = requests.post(SERVER_URL + 'update_rating', json=data, headers=test_login.headers)
    assert response.status_code == 200

def test_get_average_rating():
    response = requests.get(SERVER_URL + 'average_rating')
    assert response.status_code == 200
    assert isinstance(response.json(), list)
