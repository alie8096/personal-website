from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField,  SelectField, DateField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email
from blog.models import Category
from flask_wtf import FlaskForm
from datetime import datetime
from blog.models import Post


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
    category = SelectField("Category", choices=[], validators=[DataRequired()])
    submit = SubmitField("Create")
    
    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name) for category in Category.query.all()]
    
    
class EditNewPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    status = SelectField("Status", choices=[("draft", "Draft"), ("published", "Published"), ("archived", "Archived"), ("rejected", "Rejected")], validators=[DataRequired()])
    create_at = DateField("Create At", format=r"%Y-%m-%d", default=datetime.today, validators=[DataRequired()])
    category = QuerySelectField("Category", query_factory=lambda: Category.query.all(), get_label="name", allow_blank=True)
    submit = SubmitField("Create Post")



class EditPostForm(EditNewPostForm):
    def __init__(self, post_id, *args, **kwargs):
        super(EditPostForm, self).__init__(*args, **kwargs)
        post = Post.query.get_or_404(post_id)
        self.title.data = post.title
        self.content.data = post.content
        self.status.data = post.status
        self.category.data = post.category.id



class EditProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Update Profile")