from flask import g
from flask import render_template, Blueprint, redirect, url_for
from flask import json

from Maktab_Group_Flask_Project.models import Post, User, Category, Tag

bp = Blueprint("API", __name__)


@bp.route('/list-post/')
def list_post():
    all_post = Post.objects.all()
    json_posts = json.loads(all_post.to_json())
    for post in json_posts:
        post['author'] = User.objects(pk=post['author']['$oid']).first().username
        post['category'] = str(Category.objects(pk=post['category']['$oid']).first().name)
    return json.dumps(json_posts)


@bp.route('/delete_post/<variable>', methods=['POST', 'GET'])
def delete_post(variable):
    post = Post.objects(id=variable).first()
    if post:
        Tag.objects(posts=post).update(pull__posts=post)
        post.delete()
    return redirect(url_for("user.post_list"))


@bp.route('/deactivate_post/<variable>', methods=['POST', 'GET'])
def deactivate_post(variable):
    post = Post.objects(id=variable).first()
    if post.is_active:
        post.update(is_active=False)
    else:
        post.update(is_active=True)
    return redirect(url_for('user.post_list'))
