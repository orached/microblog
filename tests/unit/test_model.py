import pytest

def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email and avatar are defined correctly
    """
    assert new_user.email == 'john@example.com'
    assert new_user.avatar(128) == ('https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
                                        '?d=identicon&s=128')
    assert new_user.followed.all() == []
    assert new_user.followers.all() == []


def test_password_hashing(new_user):
    """
    GIVEN an existing User
    WHEN the password for the user is set
    THEN check the password is stored correctly and not as plaintext
    """
    new_user.set_password('cat')
    assert new_user.password_hash != 'cat'
    assert not new_user.check_password('dog')
    assert new_user.check_password('cat')