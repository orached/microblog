import pytest
from app import db
import time
from app.models import User, Post, Message, Notification, Task

def test_new_user(new_users):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, avatar and followed/followers are defined correctly
    """
    u = new_users[0]
    assert u.email == 'john@example.com'
    assert u.avatar(128) == ('https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
                                        '?d=identicon&s=128')
    assert u.followed.all() == []
    assert u.followers.all() == []


def test_password_hashing(new_users):
    """
    GIVEN an existing User
    WHEN the password for the user is set
    THEN check the password is stored correctly and not as plaintext
    """
    u = new_users[0]
    u.set_password('cat')
    assert u.password_hash != 'cat'
    assert not u.check_password('dog')
    assert u.check_password('cat')


def test_follow(setUp, new_users, populate_db):
    """
    GIVEN an existing user u1
    WHEN u1 is following u2
    THEN check that the followed/follower methods are set correctly
    """
    u1, u2 = new_users[0:2]

    assert u1.is_following(u2)
    assert u1.followed.count() == 2
    assert u1.followed.first().username == 'susan'
    assert u2.followers.count() == 1
    assert u2.followers.first().username == 'john'
    

def test_unfollow(setUp, new_users, populate_db):
    """
    GIVEN an existing user u1 following two users u2 and u4
    WHEN u1 unfollow u2
    THEN check that the counter of u1 followed users and u2 followers is reduced by 1
    """
    u1, u2 = new_users[0:2]

    u1.unfollow(u2)
    db.session.commit()
    assert not u1.is_following(u2)
    assert u1.followed.count() == 1
    assert u2.followers.count() == 0

def test_follow_posts(setUp, populate_db):
    """
    GIVEN 4 posts associated to 4 users
    WHEN user follows another user
    THEN check that posts from followed users and his posts are correctly called by the helper
    """
    u1, u2, u3, u4 = User.query.all()
    p1, p2, p3, p4 = Post.query.all()

    # check the followed posts of each user
    f1 = u1.followed_posts().all()
    f2 = u2.followed_posts().all()
    f3 = u3.followed_posts().all()
    f4 = u4.followed_posts().all()
    assert f1 == [p2, p4, p1]
    assert f2 == [p2, p3]
    assert f3 == [p3, p4]
    assert f4 == [p4]


def test_confirmation_token(setUp, new_users, populate_db):
    u1, u2 = new_users[0:2]
    """
    GIVEN a new visitor
    WHEN a submit successfully the registration form
    THEN a confirmation token is created
    """
    token1 = u1.get_confirm_token()
    assert u1.verify_confirm_token(token1)

    """
    GIVEN 2 different visitors
    WHEN both submit successfully the registration form
    THEN the confirmation token is different for each user
    """
    token2 = u2.get_confirm_token()
    u = u2.verify_confirm_token(token1)
    assert not (u.username == 'susan')
    assert u2.verify_confirm_token(token2)


@pytest.mark.skip(reason='to long to be executed each build. Run manualy')
def test_confirmation_token_expiration(setUp, new_users, populate_db):
    """
    GIVEN a new visitor
    WHEN a submit successfully the registration form
    THEN a confirmation token is created
    """
    u1 = new_users[0]
    token1 = u1.get_confirm_token()
    time.sleep(605)
    assert not u1.verify_confirm_token(token1)


def test_reset_password_token(setUp, new_users, populate_db):
    u1, u2 = new_users[0:2]
    """
    GIVEN a user
    WHEN he asks for password reset
    THEN a password reset token is created
    """
    token1 = u1.get_reset_password_token()
    assert u1.verify_reset_password_token(token1)

    """
    GIVEN 2 different users
    WHEN both ask for passwprd reset
    THEN the reset password token is different for each user
    """
    token2 = u2.get_reset_password_token()
    u = u2.verify_reset_password_token(token1)
    assert not (u.username == 'susan')
    assert u2.verify_reset_password_token(token2)


@pytest.mark.skip(reason='to long to be executed each build. Run manualy')
def test_reset_password_token_expiration(setUp, new_users, populate_db):  
    """
    GIVEN a user
    WHEN he didn't access the email by the delay allowed 
    THEN the reset password token expires
    """
    u1 = new_users[0]
    token1 = u1.get_reset_password_token()
    time.sleep(605)
    assert not u1.verify_reset_password_token(token1)


def test_new_message():
    """
    GIVEN a Message model
    WHEN a new Message is created
    THEN check that its attributes are set correctly
    """
    
    # TBD
    return True


def test_new_notification():
    """
    GIVEN a Notification model
    WHEN a new Notification is created
    THEN check that its attributes are set correctly
    """
    
    # TBD
    return True