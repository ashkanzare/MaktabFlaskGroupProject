import shutil

import flask

from flask import Blueprint, redirect, url_for

from Maktab_Group_Flask_Project.utils.extra_functions import find_categories

from mongoengine import Q

from flask import json

from Maktab_Group_Flask_Project.models import Post, User, Category, Tag

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


@bp.route('/delete_post/<variable>', methods=['POST', 'GET'])
def delete_post(variable):
    post = Post.objects(id=variable).first()
    if post:
        Tag.objects(posts=post).update(pull__posts=post)
        if post.image != '':
            shutil.rmtree(f"static/{'/'.join(post.image.split('/')[:3])}")
        post.delete()
    return redirect(url_for('user.post_list'))


@bp.route('/deactivate_post/<variable>/')
def deactivate_post(variable):
    """ deactivate post with the given id """
    post = Post.objects(id=variable).first()
    if post.is_active:
        post.update(is_active=False)
    else:
        post.update(is_active=True)
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


@bp.route('/search/<variable>')
def search(variable):
    """ return results of search """
    all_posts = Post.objects(Q(content__contains=variable) |
                             Q(title__contains=variable) |
                             Q(tags__name__contains=variable) |
                             Q(author__username__contains=variable))
    json_posts = json.loads(all_posts.to_json())
    return flask.jsonify(results=json_posts)
