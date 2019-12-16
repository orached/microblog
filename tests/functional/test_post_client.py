import pytest


def test_managepost_page(setUp, populate_db):
    response = setUp.get('/managepost')
    assert response.status_code == 302
    response = setUp.get('/managepost', follow_redirects=True)
    assert b"Please log in to access this page." in response.data
    # login with john's account
    response = setUp.post('/auth/login', data={
        'username': 'john',
        'password': 'cat'
    }, follow_redirects=True)
    response = setUp.get('/managepost', follow_redirects=True)
    assert b"Hi, john" in response.data
    response = setUp.post('/managepost', data={
        'title': 'My second post',
        'post': 'Amazing content here'
    })
    assert response.status_code == 302