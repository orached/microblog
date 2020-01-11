import pytest


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


def test_follow_user(setUp, populate_db):
    """
    GIVEN an anonymous User
    WHEN he tries to access follow user page
    THEN he is redirected to login page
    """
    response = setUp.get('/follow/susan', follow_redirects=True)
    assert b"Please log in to access this page." in response.data
    # login with john's account
    response = setUp.post('/auth/login', data={
        'username': 'john',
        'password': 'cat'
    }, follow_redirects=True)

    """
    GIVEN an authenticated User
    WHEN he tries to follow himself
    THEN an error message is displayed
    """
    response = setUp.get('/follow/john', follow_redirects=True)
    assert b"You cannot follow yourself!" in response.data
    
    """
    GIVEN an authenticated User
    WHEN he tries to follow an inexistent user
    THEN an error message is displayed
    """
    response = setUp.get('/follow/inexistent', follow_redirects=True)
    assert b"User inexistent not found." in response.data
    
    """
    GIVEN an authenticated User
    WHEN he tries to follow a different user
    THEN it's processed correctly
    """
    response = setUp.get('/follow/susan', follow_redirects=True)
    assert b"You are following susan!" in response.data


def test_unfollow_user(setUp, populate_db):
    """
    GIVEN an anonymous User
    WHEN he tries to access unfollow user page
    THEN he is redirected to login page
    """
    response = setUp.get('/unfollow/susan', follow_redirects=True)
    assert b"Please log in to access this page." in response.data
    # login with john's account
    response = setUp.post('/auth/login', data={
        'username': 'john',
        'password': 'cat'
    }, follow_redirects=True)
    
    """
    GIVEN an authenticated User
    WHEN he tries to unfollow himself
    THEN an error message is displayed
    """
    response = setUp.get('/unfollow/john', follow_redirects=True)
    assert b"You cannot unfollow yourself!" in response.data
    
    """
    GIVEN an authenticated User
    WHEN he tries to unfollow an inexistent user
    THEN an error message is displayed
    """
    response = setUp.get('/unfollow/inexistent', follow_redirects=True)
    assert b"User inexistent not found." in response.data
    
    """
    GIVEN an authenticated User
    WHEN he tries to unfollow a different user
    THEN it's processed correctly
    """
    response = setUp.get('/unfollow/susan', follow_redirects=True)
    assert b"You are not following susan." in response.data


def test_send_message(setUp, populate_db):
    """
    GIVEN an anonymous User
    WHEN he tries to send a message
    THEN he is redirected to login page
    """
    response = setUp.get('/send_message/susan', follow_redirects=True)
    assert b"Please log in to access this page." in response.data
    # login with john's account
    response = setUp.post('/auth/login', data={
        'username': 'john',
        'password': 'cat'
    }, follow_redirects=True)
    
    """
    GIVEN an authenticated User
    WHEN he tries to send a message to a different user
    THEN it's processed correctly
    """
    response = setUp.post('/send_message/susan', data={
            'message': 'Hi susan! I like your posts.'
        }, follow_redirects=True)
    assert b"Your message has been sent." in response.data
    response = setUp.get('/auth/logout', follow_redirects=True)

    """
    GIVEN an authenticated User
    WHEN he receives a new message
    THEN it appears in navigation bar and he can read the message in messages page
    """
    # login with susan's account
    response = setUp.post('/auth/login', data={
        'username': 'susan',
        'password': 'dog'
    }, follow_redirects=True)
    response = setUp.get('/notifications')
    assert b"\"data\": 1" in response.data
    response = setUp.get('/messages')
    assert b"john" in response.data
    assert b"Hi susan! I like your posts." in response.data