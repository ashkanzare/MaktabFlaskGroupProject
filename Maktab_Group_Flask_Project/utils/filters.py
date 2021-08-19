from flask import Blueprint

bp = Blueprint("filters", __name__)


@bp.app_template_filter('make_caps')
def caps(date):
    """Convert a Christian date to Jalali date"""
    pass
