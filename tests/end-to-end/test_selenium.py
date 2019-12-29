import pytest
import re

def test_home_page(setUp_selenium, populate_db):
    """
    GIVEN a new visitor
    WHEN he access to home page
    THEN posts are displayed
    """
    setUp_selenium.get("http://localhost:5000")
    assert re.search('<p>post from john</p>',
                                  setUp_selenium.page_source)


def test_login_page(setUp_selenium, populate_db):
    """
    GIVEN a new visitor
    WHEN he tries to login
    THEN it's processed correctly
    """
    setUp_selenium.get("http://localhost:5000")
    # navigate to login page
    setUp_selenium.find_element_by_link_text('Login').click()
    re.search('<h1>Sign In</h1>', setUp_selenium.page_source)
    # log in
    setUp_selenium.find_element_by_name('username').\
    send_keys('john')
    setUp_selenium.find_element_by_name('password').send_keys('cat')
    setUp_selenium.find_element_by_name('submit').click()
    assert re.search('<p>post from susan</p>',
                                  setUp_selenium.page_source)
    assert re.search('Logout', setUp_selenium.page_source)
    # navigate to logout page
    setUp_selenium.find_element_by_link_text('Logout').click()


def test_registration_page(setUp_selenium):
    """
    GIVEN a new visitor
    WHEN he tries to register
    THEN it's processed correctly
    """
    setUp_selenium.get("http://localhost:5000")
    # navigate to registration page
    setUp_selenium.find_element_by_link_text('Login').click()
    setUp_selenium.find_element_by_link_text('Click to Register!').click()
    # register
    setUp_selenium.find_element_by_name('username').\
    send_keys('donald')
    setUp_selenium.find_element_by_name('email').\
    send_keys('donald@example.com')
    setUp_selenium.find_element_by_name('password').send_keys('duck')
    setUp_selenium.find_element_by_name('password2').send_keys('duck')
    setUp_selenium.find_element_by_name('submit').click()
    assert re.search('A confirmation email has been sent to you by email.',
                                  setUp_selenium.page_source)
    # login with the registred user
    setUp_selenium.find_element_by_name('username').\
    send_keys('donald')
    setUp_selenium.find_element_by_name('password').send_keys('duck')
    setUp_selenium.find_element_by_name('submit').click()
    setUp_selenium.find_element_by_link_text('Posts').click()
    assert re.search('You have not confirmed your account yet.',
                                  setUp_selenium.page_source)
    setUp_selenium.find_element_by_link_text('Profile').click()
    assert re.search('You have not confirmed your account yet.',
                                  setUp_selenium.page_source)  


@pytest.mark.skip(reason='Must learn more about how to test summernote field')
def test_post_creation(setUp_selenium, populate_db):
    """
    GIVEN a registred user
    WHEN he tries to add a new post
    THEN it's processed correctly
    """
    setUp_selenium.get("http://localhost:5000")
    # navigate to login page
    setUp_selenium.find_element_by_link_text('Login').click()
    # log in
    setUp_selenium.find_element_by_name('username').\
    send_keys('john')
    setUp_selenium.find_element_by_name('password').send_keys('cat')
    setUp_selenium.find_element_by_name('submit').click()
    # navigate to post management page
    setUp_selenium.find_element_by_link_text('Posts').click()
    setUp_selenium.find_element_by_name('title').\
    send_keys('Post with selenium webdriver')
    setUp_selenium.find_element_by_name('post').\
    send_keys('This is a post created by an automated test case with Selenium webdriver')
    setUp_selenium.find_element_by_name('submit').click()
    assert re.search('Your post is now live',
                                  setUp_selenium.page_source)


def test_send_message(setUp_selenium, populate_db):
    """
    GIVEN an authenticated user
    WHEN he sent a message to a registred user
    THEN it's processed correctly
    """
    setUp_selenium.get("http://localhost:5000")
    # navigate to login page
    setUp_selenium.find_element_by_link_text('Login').click()
    # log in
    setUp_selenium.find_element_by_name('username').\
    send_keys('john')
    setUp_selenium.find_element_by_name('password').send_keys('cat')
    setUp_selenium.find_element_by_name('submit').click()
    # navigate to susan profile page
    setUp_selenium.find_element_by_link_text('susan').click()
    setUp_selenium.find_element_by_link_text('Send private message').click()
    setUp_selenium.find_element_by_name('message').\
    send_keys('Message sent to susan from john via selenium webdriver')
    setUp_selenium.find_element_by_name('submit').click()
    assert re.search('Your message has been sent.',
                                  setUp_selenium.page_source)
    # navigate to logout page
    setUp_selenium.find_element_by_link_text('Logout').click()
    # navigate to login page
    setUp_selenium.find_element_by_link_text('Login').click()
    # log in with Susan account
    setUp_selenium.find_element_by_name('username').\
    send_keys('susan')
    setUp_selenium.find_element_by_name('password').send_keys('dog')
    setUp_selenium.find_element_by_name('submit').click()
    setUp_selenium.find_element_by_partial_link_text('Messages').click()
    assert "Message sent to susan from john via selenium webdriver" in setUp_selenium.page_source
    
    


def test_follow_unfollow(setUp_selenium, populate_db):
    """
    GIVEN an authenticated user
    WHEN he follow or unfollow a user
    THEN it's processed correctly
    """
    setUp_selenium.get("http://localhost:5000")
    # navigate to login page
    setUp_selenium.find_element_by_link_text('Login').click()
    # log in
    setUp_selenium.find_element_by_name('username').\
    send_keys('john')
    setUp_selenium.find_element_by_name('password').send_keys('cat')
    setUp_selenium.find_element_by_name('submit').click()
    # navigate to susan profile page
    setUp_selenium.find_element_by_link_text('mary').click()
    setUp_selenium.find_element_by_link_text('Follow').click()
    assert 'You are following mary!' in setUp_selenium.page_source
    setUp_selenium.get("http://localhost:5000")
    setUp_selenium.find_element_by_link_text('susan').click()
    setUp_selenium.find_element_by_link_text('Unfollow').click()
    assert 'You are not following susan.' in setUp_selenium.page_source
    
    #assert '<p>post from mary</p>' in setUp_selenium.page_source
    #assert '<p>post from susan</p>' not in setUp_selenium.page_source
