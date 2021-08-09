from flask import render_template, session, request, redirect, url_for, flash, Blueprint

bp = Blueprint("home", __name__)


# blueprinte home baraye neshan dadan sadheye khoshamad gooyi
# front in bakhsh tavasote aghaye sahrayi anjam mishavad
@bp.route('/')
def home():
    return render_template('home/home.html', username=None)

