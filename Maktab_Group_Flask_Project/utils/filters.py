from flask import Blueprint

bp = Blueprint("filters", __name__)


@bp.app_template_filter('check')
def check(str_1, str_2):
    """check if two strings are same or not"""
    print(str_1.strip() == str_2.strip())
