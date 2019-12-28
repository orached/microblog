from app import create_app, db, cli
from app.models import User, Post, Message, Notification, Task, Comment, Category
import os
from flask_migrate import upgrade

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Message': Message,
            'Notification': Notification, 'Task': Task, 'Comment': Comment, 'Category': Category}


@app.cli.command()
def deploy():
    '''Run deployment tasks.'''
    # Migrate database to latest version
    upgrade()

    # Create or update post categories
    Category.insert_categories()