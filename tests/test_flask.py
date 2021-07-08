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


@pytest.mark.parametrize("list_type,response_code", [("top_rated", 200),
                                               ("now_playing", 200),
                                               ("upcoming", 200),
                                               ("popular", 200)])
def test_list_type_url(monkeypatch, list_type, response_code):
    api_mock = Mock(return_value={'results': []})

    monkeypatch.setattr("tmdb_client.call_tmdb_api", api_mock)

    with app.test_client() as client:
        response = client.get("/?list_type=" + list_type)
        assert response.status_code == response_code
        api_mock.assert_called_once_with("movie/" + list_type)
