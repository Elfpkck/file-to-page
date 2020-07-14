"""Pretty HTML's tests. PEP-8 is violated for better reading."""

from typing import TYPE_CHECKING

import pytest
from flask_api import status

from http_file_to_page import app

if TYPE_CHECKING:
    from flask.testing import FlaskClient


@pytest.fixture(scope='module')
def http_client() -> 'FlaskClient':
    return app.test_client()


def test_404(http_client: 'FlaskClient'):
    response = http_client.get('/file4.txt/wrong-url')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json == {
        'error': '404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'}


def test_405(http_client: 'FlaskClient'):
    response = http_client.post('/')
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert response.json.get('error') == 'POST is not allowed'


def test_500(http_client: 'FlaskClient'):
    response = http_client.get('/wrong-filename')
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json == {"code": 500, "error": "an error has occurred"}


def test_get_page_from_file(http_client: 'FlaskClient'):
    response = http_client.get('/file4.txt')
    assert response.status_code == status.HTTP_200_OK
