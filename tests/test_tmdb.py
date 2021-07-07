
import requests
import tmdb_client
from unittest.mock import Mock


def test_get_movies_list(monkeypatch):
    # Lista, którą będzie zwracać przysłonięte "zapytanie do API"
    mock_movies_list = ['Movie 1', 'Movie 2']
    requests_mock = Mock()
    # Wynik wywołania zapytania do API
    response = requests_mock.return_value
    # Przysłaniamy wynik wywołania metody .json()
    response.json.return_value = mock_movies_list
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)
    movies_list = tmdb_client.get_movies_list(list_type="popular")
    assert movies_list == mock_movies_list


def test_get_single_movie(monkeypatch):
    single_movie = ['Title', 'Armageddon']
    requests_mock = Mock()
    response = requests_mock.return_value
    response.json.return_value = single_movie
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)
    movie = tmdb_client.get_single_movie(15)
    assert movie == single_movie


def test_get_movie_images(monkeypatch):
    movie_images = ['id', 'dupa.jpg']
    requests_mock = Mock()
    response = requests_mock.return_value
    response.json.return_value = movie_images
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)
    images = tmdb_client.get_movie_images(15)
    assert images == movie_images


def test_get_single_movie_cast(monkeypatch):
    movie_cast = {'cast': ['brad pitt']}
    requests_mock = Mock()
    response = requests_mock.return_value
    response.json.return_value = movie_cast
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)
    cast = tmdb_client.get_single_movie_cast(15)
    assert cast == ['brad pitt']


def call_tmdb_api(endpoint):
    full_url = f"https://api.themoviedb.org/3/{endpoint}"
    headers = {
        "Authorization": f"Bearer {tmdb_client.API_TOKEN}"
    }
    response = requests.get(full_url, headers=headers)
    response.raise_for_status()
    return response.json()
