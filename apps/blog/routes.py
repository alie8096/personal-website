from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask import render_template, url_for, flash, redirect
from werkzeug.security import check_password_hash
from blog.forms import PostForm, LoginForm
from blog.models import Post, User
from blog import app, db
from sample import super_user


def create_user():
    email = super_user["email"]
    password = super_user["password"]
    
    existing_user = User.query.filter_by(email=email).first()
    
    if existing_user is None:
        username = super_user["username"]
        password = super_user["password"]
    
        user = User(username=username, email=email, password=password)
        user.set_password(password=password)
    
        db.session.add(user)
        db.session.commit()
        
    else:
        print("User with this email already exist")
    
with app.app_context():
    create_user()


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template("home.html", posts=posts)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for("home"))
        
        flash("Login failed. Check username and/or password.", "error")
        
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", title="Profile")


@app.route("/create_post", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data)
        db.session.add(post)
        db.session.commit()
        flash("Your Post has been created!", "success")
        return redirect(url_for("home"))
    return render_template("create_post.html", title="New Post", form=form)


