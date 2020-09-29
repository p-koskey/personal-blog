from flask_wtf import FlaskForm
from flask import flash
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField,  BooleanField, TextAreaField,RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Required
from app.models import User, Post, Comments, Subscribers

class PostForm(FlaskForm):
    post_title = StringField('Title', validators = [Required()])
    post_content = TextAreaField("Blog Content", validators = [Required()])
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you:',validators = [Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
  
    description = TextAreaField('Add a comment:', validators = [Required()])
    submit = SubmitField('Submit')

class CommentForm2(FlaskForm):
    name = StringField('Enter your name:',validators = [Required()])
    description = TextAreaField('Add a comment:', validators = [Required()])
    submit = SubmitField('Submit')


class SubscribeForm(FlaskForm):  
    email = StringField(render_kw={"placeholder": "Enter your email address"},validators=[Required()])
    submit = SubmitField('Subscribe')
