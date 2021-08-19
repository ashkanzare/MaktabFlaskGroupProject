from flask import Blueprint

bp = Blueprint("filters", __name__)


@bp.app_template_filter('en_to_fa')
def en_to_fa(text):
    """convert english number to persian"""
    fa_numbers = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹']
    text_list = list(str(text))
    for i in range(len(text_list)):
        if text_list[i].isnumeric():
            text_list[i] = fa_numbers[int(text_list[i])]
    return ''.join(text_list)

