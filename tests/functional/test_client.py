import pytest
from app import db

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

def test_register_and_login(setUp):
    # login with unknown account
    response = setUp.post('/auth/login', data={
        'username': 'donald',
        'password': 'duck'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data
    assert b"Profile" not in response.data

    # register a new account
    response = setUp.post('/auth/register', data={
        'email': 'donald@example.com',
        'username': 'donald',
        'password': 'duck',
        'password2': 'duck'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Congratulations, you are now a registered user!" in response.data

    # login with the new account
    response = setUp.post('/auth/login', data={
        'username': 'donald',
        'password': 'duck'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"login" not in response.data
    assert b"Messages" in response.data

    # log out
    response = setUp.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"logout" not in response.data

def test_reset_password(setUp):
    # TBD
    response = setUp.post('/auth/reset_password_request', data={
        'email': 'donald@example.com'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Check your email for the instructions to reset your password" in response.data

def test_edit_profile(setUp, populate_db):
    """
    GIVEN an anonymous User
    WHEN he tries to access to profile edition page
    THEN he is redirected to login page
    """
    response = setUp.get('/edit_profile')
    assert response.status_code == 302
    response = setUp.get('/edit_profile', follow_redirects=True)
    assert b"Please log in to access this page." in response.data
    
    """
    GIVEN an authenticated User
    WHEN he access to profile edition page and post a modification
    THEN the profile modification is correctly processed
    """
    # login with john's account
    response = setUp.post('/auth/login', data={
        'username': 'john',
        'password': 'cat'
    }, follow_redirects=True)
    #john change his username to jojo
    response = setUp.post('/edit_profile', data={
        'username': 'jojo'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Your changes have been saved." in response.data