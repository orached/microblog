from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_babel import _, lazy_gettext as _l


class PostForm(FlaskForm):
    title = StringField(_l('Title'), id="post_title", validators=[DataRequired()])
    post = TextAreaField(_l('Content'), id="post_body", validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

class CommentForm(FlaskForm):
    comment = StringField(_l('Enter your comment'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))