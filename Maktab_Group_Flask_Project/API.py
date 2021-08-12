from flask import g
from flask import render_template, Blueprint
from flask import json


from Maktab_Group_Flask_Project.models import Post, User, Category

bp = Blueprint("API", __name__)


@bp.route('/list-post/')
def list_post():
    all_post = Post.objects.all()
    json_posts = json.loads(all_post.to_json())
    for post in json_posts:
        post['author'] = User.objects(pk=post['author']['$oid']).first().username
        post['category'] = str(Category.objects(pk=post['category']['$oid']).first().name)
    return json.dumps(json_posts)
