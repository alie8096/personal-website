from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField,  SelectField, DateField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")
    
    
class CreatePostForm(FlaskForm):
    title = StringField("title", validators=[DataRequired()])
    content = TextAreaField("content", validators=[DataRequired()])
    status = SelectField("status", choices=[("draft", "Draft"), ("published", "Published"), ("archived", "Archived"), ("rejected", "Rejected")], validators=[DataRequired()])
    create_at = DateField("Create At", format=r"%Y-%m-%d", default=datetime.today, validators=[DataRequired()])
    submit = SubmitField("Create")
    

class EditProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Update Profile")