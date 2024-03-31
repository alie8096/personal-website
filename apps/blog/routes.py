from functools import wraps
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask import render_template, url_for, flash, redirect, request
from blog.forms import CreatePostForm, LoginForm
from blog.models import Post, User
from sample import SUPER_USER
from blog import app, db




def create_user():
    email = SUPER_USER.email
    password = SUPER_USER.password
    username = SUPER_USER.username
    is_admin = SUPER_USER.is_admin

    existing_user = User.query.filter_by(email=email).first()
    
    if existing_user:
        print(f"User with email already exists.")
    else:
        user = User(username=username, email=email)
        # Set password securely using generate_password_hash
        user.password = password
        user.is_admin = is_admin

        db.session.add(user)
        db.session.commit()
        
        print(f"User created successfully!")

# with app.app_context():
    # create_user()
    

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
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            # user.is_admin = user.check_admin()
            # db.session.commit()
            flash("Login is successfully", "success")
            print("Login is successfully", "success")
            return redirect(url_for("admin"))
        flash("Login failed. Check username and/or password", "error")
        print("Login failed. Check username and/or password", "error")
        
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


@app.route("/admin")
def admin():
    if current_user.is_admin:
        return render_template("admin.html")
    else:
        return redirect(url_for("home"))

def admin_required(f):
    @login_required
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            return redirect(url_for("home"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/admin/posts")
def admin_posts():
    posts = Post.query.all()
    return render_template("admin_posts.html", posts=posts)

@app.route("/admin/posts/new")
def admin_post_new():
    return render_template("admin_posts_new.html")


@app.route("/admin/posts/create", methods=["GET", "POST"])
@login_required
@admin_required
def admin_posts_create():
    form = CreatePostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        status = form.status.data
        create_at = form.create_at.data
        author = current_user.id
    
        post = Post(title=title, content=content, status=status, create_at=create_at, author=author)
        db.session.add(post)
        db.session.commit()
    
        flash("Post create successfully!", "success")
        return redirect(url_for("admin_posts"))
    
    return render_template("admin_posts_create.html", title="Create Post", form=form)
    

@app.route("/admin/posts/<int:id>/edit")
def admin_post_edit(id):
    post = Post.query.get_or_404(id)
    return render_template("admin_posts_edit.html")


@app.route("/admin/posts/<int:id>/update", methods=["POST"])
def admin_posts_update(id):
    post = Post.query.get_or_404(id)
    
    post.title = request.form["title"]
    post.content = request.form["content"]
    post.status = request.form["status"]
    
    # post.date_posted #TODO
    
    db.session.commit()
    
    return redirect(url_for("admin_posts"))


@app.route("/admin/posts/<int:id>/delete")
def admin_posts_delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    
    return redirect(url_for("admin_posts"))