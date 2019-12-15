import pytest


def test_managepost_page(setUp):
    response = setUp.get('/managepost')
    assert response.status_code == 302
    response = setUp.get('/managepost', follow_redirects=True)
    assert b"Please log in to access this page." in response.data