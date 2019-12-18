import pytest


def test_register(setUp, populate_db):
    """
    GIVEN an already registred user
    WHEN some one tries to use the same username and/or email
    THEN error messages are prompt to ask user to choose differents logins
    """
    response = setUp.post('/auth/register', data={
        'email': 'john@example.com',
        'username': 'john',
        'password': 'cat',
        'password2': 'cat'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Congratulations" not in response.data
    assert b"Please use a different username." in response.data
    assert b"Please use a different email address." in response.data

    """
    GIVEN a never used email and username
    WHEN user fill the registration form
    THEN a message appear on the GUI
    """
    response = setUp.post('/auth/register', data={
        'email': 'donald@example.com',
        'username': 'donald',
        'password': 'duck',
        'password2': 'duck'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"A confirmation email has been sent to you by email." in response.data


def test_login(setUp, populate_db):
    """
    GIVEN an unknown username or false password
    WHEN user tries to login
    THEN an error message appear
    """
    response = setUp.post('/auth/login', data={
        'username': 'donald',
        'password': 'duck'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data
    assert b"Profile" not in response.data

    """
    GIVEN a registred user
    WHEN he tries to login with correct identifiers
    THEN he is correctly logged in
    """
    response = setUp.post('/auth/login', data={
        'username': 'john',
        'password': 'cat'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"login" not in response.data
    assert b"Messages" in response.data

    """
    GIVEN a logged user
    WHEN he tries to logout
    THEN he is correctly logged out
    """
    response = setUp.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"logout" not in response.data


def test_reset_password(setUp, populate_db):
    """
    GIVEN a non stored email
    WHEN it's used to reset a password
    THEN an error message appear
    """
    response = setUp.post('/auth/reset_password_request', data={
        'email': 'donald@example.com'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"This email is unknown. Please use email you registred with." in response.data

    """
    GIVEN a stored email
    WHEN it's used to reset a password
    THEN an email with instructions is sent
    """
    response = setUp.post('/auth/reset_password_request', data={
        'email': 'john@example.com'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Check your email for the instructions to reset your password" in response.data