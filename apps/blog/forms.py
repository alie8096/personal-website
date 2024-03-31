from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField("title", validators=[DataRequired()])
    content = TextAreaField("content", validators=[DataRequired()])
    submit = SubmitField("Post")
    

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")