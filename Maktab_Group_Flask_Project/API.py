import flask
from flask import g
from flask import render_template, Blueprint, redirect, url_for
from flask import json, jsonify

from Maktab_Group_Flask_Project.models import Post, User, Category, Tag

from Maktab_Group_Flask_Project.utils.extra_functions import find_categories
bp = Blueprint("API", __name__)


@bp.route('/list-post/')
def list_post():
    """ return json of all active posts """
    all_post = Post.objects(is_active=True)
    json_posts = json.loads(all_post.to_json())
    for post in json_posts:
        post['author'] = User.objects(pk=post['author']['$oid']).first().username
        post['category'] = str(Category.objects(pk=post['category']['$oid']).first().name)
    return flask.jsonify(json_posts)


@bp.route('/delete_post/<variable>/')
def delete_post(variable):
    # todo: if a post deleted then delete it reference from tags
    """ delete post with the given id """
    post = Post.objects(id=variable).first()
    if post:
        Tag.objects(posts=post).update(pull__posts=post)
        post.delete()
    return redirect(url_for('user.post_list'))


@bp.route('/deactivate_post/<variable>/')
def deactivate_post(variable):
    """ deactivate post with the given id """
    post = Post.objects(id=variable).first()
    if post.is_active:
        post.update(is_actice=False)
    else:
        post.update(is_actice=True)
    post.save()
    return redirect(url_for('user.post_list'))


@bp.route('/list-categories/')
def list_categories():
    """ return list of categories """
    all_categories = Category.objects(__raw__={"path": {"$regex": fr"^0\/[^\/]*$"}})
    json_categories = json.loads(all_categories.to_json())
    find_categories(json_categories)
    return flask.jsonify(json_categories)


@bp.route('/list-tags/')
def list_tags():
    """ return list of tags """
    all_tags = Tag.objects()
    json_tags = json.loads(all_tags.to_json())
    return flask.jsonify(json_tags)

