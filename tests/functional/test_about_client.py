import pytest


def test_about_page(setUp):
    response = setUp.get('/about')
    assert response.status_code == 200
    assert b"QA engineer" in response.data