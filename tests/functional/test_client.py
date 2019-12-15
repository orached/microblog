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
    # register a new account
    response = setUp.post('/auth/register', data={
        'email': 'donald@example.com',
        'username': 'donald',
        'password': 'duck',
        'password2': 'duck'
    })
    assert response.status_code == 302

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
    
