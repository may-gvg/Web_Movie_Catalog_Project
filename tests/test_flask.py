import pytest
from main import app
from unittest.mock import Mock



def test_homepage(monkeypatch):
    api_mock = Mock(return_value={'results': []})
    monkeypatch.setattr("tmdb_client.call_tmdb_api", api_mock)

    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        api_mock.assert_called_once_with('movie/popular')


@pytest.mark.parametrize("url,response_code", [("/?list_type=top_rated'", 200), ("/?list_type=now_playing'", 200), ("/?list_type=upcoming'", 200), ("/?list_type=popular", 200)])
def test_page(monkeypatch, url, response_code):
    api_mock = Mock(return_value={'results': []})
    monkeypatch.setattr("tmdb_client.call_tmdb_api", api_mock)

    with app.test_client() as client:
        response = client.get(url)
        assert response.status_code == response_code

