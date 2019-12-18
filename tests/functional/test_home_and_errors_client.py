import pytest

def test_home_page(setUp):
    response = setUp.get('/')
    assert response.status_code == 200
    response = setUp.get('/index')
    assert response.status_code == 200

def test_404_page(setUp):
    response = setUp.get('/inexistent')
    assert response.status_code == 404
    assert b"Not Found" in response.data


def test_500_page(setUp):
    # TBD
    return True

