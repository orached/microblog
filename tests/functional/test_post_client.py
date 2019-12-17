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
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Your post is now live!" in response.data

def test_editpost_page(setUp, populate_db):
    response = setUp.get('/editpost/1')
    assert response.status_code == 302
    # login with john's account
    response = setUp.post('/auth/login', data={
        'username': 'john',
        'password': 'cat'
    }, follow_redirects=True)
    response = setUp.get('/editpost/1', follow_redirects=True)
    assert b"Edit post" in response.data
    response = setUp.post('/editpost', data={
        'title': 'My second post',
        'post': 'Amazing content here'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Your post is now live!" in response.data