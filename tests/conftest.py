import pytest
from app import create_app, db
from app.models import User

@pytest.fixture()
def new_user():
    u = User(username='john', email='john@example.com')
    return u


@pytest.fixture()
def setUp():
    app = create_app('testing')
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    client = app.test_client(use_cookies=True)
    
    yield client
    
    db.session.remove()
    db.drop_all()
    app_context.pop()