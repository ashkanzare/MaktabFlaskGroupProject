import datetime
import shutil

import flask

from flask import Blueprint, redirect, url_for, request, g, render_template, flash

from Maktab_Group_Flask_Project.blog import login_required
from Maktab_Group_Flask_Project.utils.extra_functions import find_categories, set_likes_count

from mongoengine import Q

from flask import json

from Maktab_Group_Flask_Project.models import Post, User, Category, Tag, Comment, LikeDislike


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
        # if post.image != '':
        #     shutil.rmtree(f"static/{'/'.join(post.image.split('/')[:3])}")
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
    all_tags = Tag.objects().order_by('-id')[:6]
    json_tags = json.loads(all_tags.to_json())
    return flask.jsonify(json_tags)


@bp.route('/search/<variable>')
def search(variable):
    """ return results of search """
    user_search = User.objects(username__contains=variable).first()
    all_posts = Post.objects(Q(content__contains=variable) |
                             Q(title__contains=variable) |
                             Q(tags__name__contains=variable) |
                             Q(author=user_search))
    json_posts = json.loads(all_posts.to_json())
    return flask.jsonify(results=[{'_id': post['_id'], 'title': post['title'], 'author': User.objects(pk=post['author']['$oid']).first().username, 'image': post['image']} for post in json_posts])


@bp.route('/post-comments/<variable>')
def post_comments(variable):
    """ return comments of a post """
    counter = int(request.args['counter'])
    comments = Comment.objects(post=variable)
    comment_select = comments.order_by('-id')[:5 * counter]
    top_3_update = comments.order_by('-id')[:3]
    json_comments = json.loads(comment_select.to_json())
    return flask.jsonify(result=json_comments, time=int(datetime.datetime.utcnow().timestamp() * 1000),
                         max=len(comments), top_3=json.loads(top_3_update.to_json()))


@bp.route('/user-profile/<variable>')
def user_profile(variable):
    """ return userprofile and 6 post from the same user """
    user = User.objects(username=variable).first()
    posts_user = Post.objects(author=user.id)
    return render_template('user/user_profile.html', user=user, posts_user=posts_user)


@bp.route('/post-action/', methods=['POST', 'GET'])
def post_action():
    """ submit like, dislike """
    if g.user:
        data = request.args
        action = True if data['value'] == 'like' else False
        post = Post.objects(pk=data['post']).first()
        post_act = LikeDislike.objects(post=post, user=g.user).first()
        if post_act:
            if post_act.value == action:
                post_act.delete()
                set_likes_count(post)
                status = 'undone'
            else:
                post_act.value = action
                post_act.save()
                set_likes_count(post)
                status = 'reverse'

        else:
            new_action = LikeDislike(post=post, user=g.user, value=action)
            new_action.save()
            set_likes_count(post)
            status = 'done'

        return flask.jsonify(json.loads(json.dumps({'status': status, 'likes': post.likes_count, 'dislikes': post.dislikes_count})))
    else:
        flash('ابتدا باید وارد شوید', 'text-danger')
        return redirect(url_for("blog.login"))
