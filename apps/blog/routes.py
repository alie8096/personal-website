from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from blog.forms import EditNewPostForm, LoginForm, EditProfileForm, CreatePostForm
from flask import render_template, url_for, flash, redirect, request
from blog.models import Post, User
from blog.models import Category
from sample import SUPER_USER
from functools import wraps
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
    

@app.route("/")
@app.route("/home")
def home():
    last_three_posts = Post.query.order_by(Post.date_posted.desc()).limit(3).all()
    return render_template("home.html", posts=last_three_posts)


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
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("Login is successfully", "success")
            return redirect(url_for("admin"))
        flash("Login failed. Check username and/or password", "error")       
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



def admin_required(f):
    @login_required
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            return redirect(url_for("home"))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/admin")
def admin():
    if current_user.is_admin:
        return render_template("admin.html")
    else:
        return redirect(url_for("home"))
    
@app.route("/admin-panel")
@login_required
@admin_required
def admin_panel():
    return render_template("admin_panel.html")

    
@app.route("/post/<int:id>")  # Public post view route
def post(id):
    post = Post.query.get_or_404(id)
    if post is None:
        flash("Post not found!", "danger")
        return redirect(url_for("home"))  # Redirect to homepage if post not found
    
    return render_template("post.html", post=post)


@app.route("/admin/post/<int:id>", methods=["GET", "POST", "DELETE"])
@login_required
@admin_required
def admin_post(id):
    post = Post.query.get_or_404(id)
    categories = Category.query.all()

    if request.method == "POST":
        if request.form["_method"] == "DELETE":
            db.session.delete(post)
            db.session.commit()
            flash("Post deleted successfully!", "success")
            return redirect(url_for("admin_posts"))
        
        form = EditNewPostForm(request.form)  # Use the same form for editing
        if form.validate():
            form.populate_obj(post)  # Update post with form data
            db.session.commit()
            flash("Post updated successfully!", "success")
            return redirect(url_for("admin_posts"))
        else:
            flash("Form validation failed", "error")
    else:
        # Populate the form with post data for editing
        form = EditNewPostForm(obj=post)

    return render_template("admin_post.html", title="Edit/Delete Post", post=post, form=form, categories=categories)




@app.route("/posts", methods=["GET"])
@login_required
@admin_required
def admin_posts():
    # posts = Post.query.all()
    posts = Post.query.filter(Post.date_posted != None).all()
    return render_template("admin_posts.html", title="All Posts", posts=posts)


@app.route("/new-post")
@login_required
@admin_required
def admin_posts_new():
  form = CreatePostForm()
  return render_template("admin_posts_new.html", form=form, categories=Category.query.all())


@app.route("/create", methods=["POST"])
@login_required
@admin_required
def admin_posts_create():
  categories = Category.query.all()
  form = CreatePostForm()

  if form.validate_on_submit():
    title = form.title.data
    content = form.content.data
    status = form.status.data
    author = current_user.id
    category_id = form.category.data

    post = Post(title=title, content=content, status=status, author=author, category_id=category_id)
    db.session.add(post)
    db.session.commit()

    flash("Post created successfully!", "success")
    return redirect(url_for("admin_posts"))

  return render_template("admin_posts_create.html", title="Create Post", form=form, categories=Category.query.all())

    

@app.route("/admin/profile", methods=["GET", "POST"])
@login_required
@admin_required
def admin_profile():
    user = User.query.get(current_user.id)
    if request.method == "POST":
        form = EditProfileForm(obj=user)
        if form.validate_on_submit():
            user.username = form.username.data
            user.email = form.email.data
            user.password = form.password.data
            db.session.commit()
            flash("Profile updated successfully!", "success")
            return redirect(url_for("admin"))
        return render_template("admin_profile.html", form=form)
    return render_template("admin_profile.html", form=EditProfileForm(obj=user))

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.route("/about")
def about_me():
    return render_template("about_me.html")