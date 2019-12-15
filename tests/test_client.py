import pytest
from app import db

def test_home_page(setUp):
    response = setUp.get('/')
    assert response.status_code == 200
    response = setUp.get('/index')
    assert response.status_code == 200

def test_register_and_login(setUp):
    # register a new account
    response = setUp.post('/auth/register', data={
        'email': 'john@example.com',
        'username': 'john',
        'password': 'cat',
        'password2': 'cat'
    })
    assert response.status_code == 302

    # login with the new account
    response = setUp.post('/auth/login', data={
        'email': 'john@example.com',
        'password': 'cat'
    }, follow_redirects=True)
    assert response.status_code == 200


    # log out
    response = setUp.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200