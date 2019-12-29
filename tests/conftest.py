import pytest
import threading
import time
from selenium import webdriver
from app import create_app, db
from app.models import User, Post, Comment, Category
from datetime import datetime, timedelta

@pytest.fixture()
def new_users():
    '''create 4 users'''
    return (
        User(username='john', email='john@example.com'),
        User(username='susan', email='susan@example.com'),
        User(username='mary', email='mary@example.com'),
        User(username='david', email='david@example.com')
    )

@pytest.fixture()
def new_posts(new_users):
    '''create 4 posts and each one to a different user'''
    u1, u2, u3, u4 = new_users
    now = datetime.utcnow()
    
    return (
        Post(body="post from john", body_html="<p>post from john</p>", author=u1,
            timestamp=now + timedelta(seconds=1)),
        Post(body="post from susan", body_html="<p>post from susan</p>", author=u2,
                timestamp=now + timedelta(seconds=4)),
        Post(body="post from mary", body_html="<p>post from mary</p>", author=u3,
                timestamp=now + timedelta(seconds=3)),
        Post(body="post from david", body_html="<p>post from david</p>", author=u4,
                timestamp=now + timedelta(seconds=2))
    )

@pytest.fixture()
def new_comments(new_users, new_posts):
    '''create 4 comments from 3 users for 2 posts'''
    u1, u2, u3, u4 = new_users
    p1, p2, p3, p4 = new_posts
    now = datetime.utcnow()
    
    return (
        Comment(body="comment from john about his same post", author=u1, post=p1,
            timestamp=now + timedelta(seconds=1)),
        Comment(body="comment from susan about john's post", author=u2, post=p1,
                timestamp=now + timedelta(seconds=4)),
        Comment(body="I like your posts Mary. Br, Susan", author=u2, post=p3,
                timestamp=now + timedelta(seconds=3)),
        Comment(body="comment from david about John's post", author=u4, post=p1,
                timestamp=now + timedelta(seconds=2))
    )

@pytest.fixture()
def setUp():
    app = create_app('testing')
    app_context = app.app_context()
    app_context.push()
    client = app.test_client(use_cookies=True)
    db.create_all()
    
    yield client
    
    db.session.remove()
    db.drop_all()
    app_context.pop()

@pytest.fixture()
def populate_db(new_users, new_posts, new_comments):
    Category.insert_categories()
    u1, u2, u3, u4 = new_users
    u1.set_password('cat')  #Set password for john
    u2.set_password('dog')  #Set password for susan
    u3.set_password('fox')  #Set password for mary
    u1.confirmed = True
    u2.confirmed = True
    db.session.add_all([u1, u2, u3, u4])
    p1, p2, p3, p4 = new_posts
    p1.category_id=1    #Set category 1 to post 1
    p2.category_id=2    #Set category 2 to post 2
    p3.category_id=3    #Set category 3 to post 3
    p4.category_id=1    #Set category 1 to post 4
    db.session.add_all([p1, p2, p3, p4])
    c1, c2, c3, c4 = new_comments
    db.session.add_all([c1, c2, c3, c4])

    # setup the followers
    u1.follow(u2)  # john follows susan
    u1.follow(u4)  # john follows david
    u2.follow(u3)  # susan follows mary
    u3.follow(u4)  # mary follows david

    db.session.commit()


@pytest.fixture()
def setUp_selenium():
    # start Chrome
    path="C:\\Users\\hpfolio\\Downloads\\chromedriver_win32\\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    try:
        driver = webdriver.Chrome(chrome_options=options, executable_path=path)
    except:
        pass
    
    # skip these tests if the browser could not be started
    if driver:
        # create the application
        app = create_app('testing')
        app_context = app.app_context()
        app_context.push()

        # suppress logging to keep unittest output clean
        import logging
        logger = logging.getLogger('werkzeug')
        logger.setLevel("ERROR")

        # create the database and populate with some fake data
        db.create_all()
        Category.insert_categories()
        db.session.commit()

        # start the Flask server in a thread
        server_thread = threading.Thread(target=app.run,
                                                kwargs={'debug': False})
        server_thread.start()

        # give the server 2 seconds to ensure it is up
        time.sleep(2) 
    
    yield driver
    
    if driver:
        # stop the flask server and the browser
        driver.get('http://localhost:5000/shutdown')
        driver.quit()
        server_thread.join()

        # destroy database
        db.drop_all()
        db.session.remove()

        # remove application context
        app_context.pop()


@pytest.fixture()
def user_logged(setUp, populate_db):
    # login with john's account
    response = setUp.post('/auth/login', data={
        'username': 'john',
        'password': 'cat'
    }, follow_redirects=True)