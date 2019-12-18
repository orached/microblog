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