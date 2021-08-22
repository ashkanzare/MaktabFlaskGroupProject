from flask import session, redirect, url_for, Blueprint, json, jsonify
from flask import flash
from flask import g
from flask import render_template
from flask import request
from werkzeug.security import check_password_hash

from Maktab_Group_Flask_Project.models import User, Category, Tag
from Maktab_Group_Flask_Project.utils.extra_functions import (
    check_photo, create_user, check_for_register_errors, lower_form_values)

import functools

from Maktab_Group_Flask_Project.models import Post

bp = Blueprint("blog", __name__)


@bp.route('/')
def home():
    """ home route for showing all posts """
    all_posts = Post.objects(is_active=True)
    return render_template('blog/blog.html', posts=all_posts.order_by('-id'))


def login_required(view):
    """View decorator that redirects anonymous users to the auth page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('ابتدا باید ثبت نام کنید', 'text-danger')
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
        g.user = User.objects(id=user_id).first()


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.
    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        user_field = lower_form_values(request)

        # get image from request
        image = request.files['file']

        # if there is any error in register store it in error
        error = check_for_register_errors(user_field['username'], user_field['password'], user_field['re_password'],
                                          user_field['email'])

        if error is None:
            if create_user(user_field, image):
                return redirect(url_for("blog.login"))

        flash(error)

    return render_template("blog/auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """ Log in a registered user by adding the user id to the session. """
    if request.method == "POST":
        username = request.form["username"].lower()
        password = request.form["password"].lower()

        # find user with the given username
        user = User.objects(username=username).first()

        error = None
        if user is None:
            error = "نام کاربری اشتباه است"
        elif not check_password_hash(user.password, password):
            error = "رمز عبور اشتباه است"

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = str(user.id)
            return redirect(url_for("blog.home"))

        flash(error, 'text-danger')

    return render_template("blog/auth/login.html")


@bp.route('/restore/', methods=['GET', 'POST'])
def restore():
    """ restore page for restoring username and password """
    return render_template('blog/auth/restore.html', info=None)


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("blog.login"))


@bp.route("/create_category")
def create_category():
    """ Create category """
    c1 = Category.objects(name='برنامه نویسی').first()
    c2 = Category(name='جاوا اسکریپت')
    c2.save()
    c2.path = f"{c1.path}/{c2.id}"
    c2.save()

    return 'category saved'


@bp.route("/category/<variable>")
def category(variable):
    """ search a category's posts """
    categories = Category.objects(path__contains=variable)
    posts = Post.objects(category__in=[cat.id for cat in categories], is_active=True).order_by('-id')
    # json_categories = json.loads(posts.to_json())
    # return jsonify(json_categories)
    return render_template('blog/blog.html', posts=posts, category=categories.first().name)


@bp.route("/tag/<variable>")
def tag(variable):
    """ search a tag's posts """
    tag_posts = Tag.objects(pk=variable).first()
    return render_template('blog/blog.html', posts=[post for post in tag_posts.posts if post.is_active],
                           tag=tag_posts.name)
