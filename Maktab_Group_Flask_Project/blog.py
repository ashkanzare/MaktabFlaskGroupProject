from flask import render_template, session, request, redirect, url_for, flash, Blueprint
from Maktab_Group_Flask_Project.models import Post
bp = Blueprint("home", __name__)


# blueprinte home baraye neshan dadan sadheye khoshamad gooyi
# front in bakhsh tavasote aghaye sahrayi anjam mishavad
@bp.route('/')
def home():
    all_posts = Post.objects(is_active=True)
    return render_template('blog/blog.html', posts=all_posts)

