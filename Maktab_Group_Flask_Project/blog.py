from flask import session, redirect, url_for, flash, Blueprint
from flask import flash
from flask import g
from flask import render_template
from flask import request
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from Maktab_Group_Flask_Project.models import User

from hashlib import sha256
import os
import functools

from Maktab_Group_Flask_Project.models import Post

bp = Blueprint("blog", __name__)


# blueprinte home baraye neshan dadan sadheye khoshamad gooyi
# front in bakhsh tavasote aghaye sahrayi anjam mishavad
@bp.route('/')
def home():
    all_posts = Post.objects(is_active=True)
    return render_template('blog/blog.html', posts=all_posts)


# front in bakhsh tavasote aghaye ebrahim zade anjam shode

def login_required(view):
    """View decorator that redirects anonymous users to the auth page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('ابتدا باید ثبت نام کنید')
            return redirect(url_for("blog.register"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            User.objects(id=user_id).first()
        )


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.
    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        users_len = User.objects().count()
        image = request.files['file']
        ext = image.filename.split('.')[-1]
        photo = ''
        if image:
            try:
                os.makedirs(f'static/media/users/user_{users_len + 1}/')
            except FileExistsError:
                pass
            path = f'static/media/users/user_{users_len + 1}/' + \
                   sha256(request.form['username'].encode()).hexdigest() + '.' + ext
            image.save(path)
            photo = path[7:]
        first_name = request.form['first_name'].lower()
        last_name = request.form['last_name'].lower()
        username = request.form['username'].lower()
        email = request.form['email'].lower()
        phone = request.form['email'].lower()
        password = request.form['password'].lower()
        re_password = request.form['re_password'].lower()
        if re_password != password:
            flash('رمز عبور با تکرار رمز یکسان نیست')
            return redirect(url_for('blog.register'))
        error = None

        if not username:
            error = "نام کاربری را وارد کنید"
        elif not password:
            error = "رمز عبور را وارد کنید"
        elif (
                User.objects(username=username).first()
                is not None
        ):
            error = f" نام کاربری {username} گرفته شده است"

        if error is None:
            # the name is available, store it in the database and go to
            # the auth page
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                phone=phone,
                photo=photo,
                password=generate_password_hash(password),
            )
            new_user.save()
            flash('ثبت نام شما با موفقیت انجام شد')
            return redirect(url_for("blog.login"))

        flash(error)

    return render_template("blog/auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"].lower()
        password = request.form["password"].lower()
        error = None
        user = User.objects(username=username).first()

        if user is None:
            error = "نام کاربری اشتباه است"
        elif not check_password_hash(user.password, password):
            error = "رمز عبور اشتباه است"

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = str(user.id)
            return redirect(url_for("blog.home"))

        flash(error)

    return render_template("blog/auth/login.html")


@bp.route('/restore/', methods=['GET', 'POST'])
def restore():
    return render_template('blog/auth/restore.html', info=None)


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("blog.login"))
