import pytest
from app import create_app, db

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