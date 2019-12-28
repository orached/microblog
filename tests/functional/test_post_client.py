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
        'category': 1,
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
    assert b"Edit Post" in response.data
    response = setUp.post('/editpost/1', data={
        'title': 'My first post',
        'category': 1,
        'post': 'First amazing content here'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"The post has been updated." in response.data


def test_category_page(setUp, populate_db):
    """
    GIVEN a visitor (authenticated or not)
    WHEN he decide to browse posts by category
    THEN posts by choosen category are displayed
    """
    response = setUp.get('/category/1')
    assert response.status_code == 200
    assert b"Category:" in response.data
    assert b"john" in response.data
    assert b"susan" not in response.data