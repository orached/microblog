from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_babel import _, lazy_gettext as _l


class PostForm(FlaskForm):
    post = TextAreaField(_l('Say something'), id="post_body", validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))