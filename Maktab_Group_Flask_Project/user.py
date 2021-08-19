from flask import render_template, request, redirect, url_for, flash, Blueprint
from Maktab_Group_Flask_Project.models import User, Tag, Category, Post
from flask import g
from werkzeug.security import generate_password_hash

from Maktab_Group_Flask_Project.utils.extra_functions import (
    check_photo, check_user_email_username, lower_form_values, tags_changes)

bp = Blueprint("user", __name__)


@bp.route('/profile/')
def profile():
    """ show user's profile information """
    return render_template('user/profile.html', user=g.user)


@bp.route('/edit-profile/', methods=['POST', 'GET'])
def edit_profile():
    """ edit user profile information """
    if request.method == 'POST':
        # get user info
        user_id = g.user.id
        user = User.objects(id=user_id).first()
        path = user.photo.split('/')

        # get user edit form values
        user_field = lower_form_values(request)

        # get image from request
        image = request.files['file']
        # make directory for user profile picture
        photo = check_photo(image, int(path[2].split('_')[-1]), 'user', 'username', default_photo=user.photo)

        if user_field['password'] != user_field['re_password']:
            flash('رمز عبور با تکرار رمز یکسان نیست', 'text-danger')
            return redirect(url_for('user.edit_profile'))

        # check if edited email and username are unique
        # if there is no error then save new changes
        check_info = check_user_email_username(user_field['username'], user_field['email'], user.id)
        if check_info == True:
            user.first_name = user_field['first_name']
            user.last_name = user_field['last_name']
            user.username = user_field['username']
            user.email = user_field['email']
            user.photo = photo
            if user_field['password'] != '':
                user.password = generate_password_hash(user_field['password'])
            user.save()

        elif check_info == "invalid_username":
            flash('نام کابری از قبل گرفته شده است', 'text-danger')
            return redirect(url_for('user.edit_profile'))

        else:
            flash('ایمیل از قبل در سیستم موجود است', 'text-danger')
            return redirect(url_for('user.edit_profile'))

        return render_template('user/profile.html', user=user)

    return render_template('user/edit_profile.html')


@bp.route('/create-post/', methods=['POST', 'GET'])
def create_post():
    """ create a post """
    if request.method == 'POST':
        try:
            check_active_exist = request.form['is_active']
            is_active = True
        except:
            is_active = False

        tags = []
        if request.form['invisible']:
            tags = request.form['invisible'].split(',')
        print('tags: ', tags)

        user = g.user
        title = request.form['title']
        content = request.form['content']
        image = request.files['file']

        category_name = request.form['category']
        category = Category.objects(name=category_name.strip()).first()

        posts_len = Post.objects().count()
        final_image = check_photo(image, posts_len, 'post', 'title')

        new_post = Post(
            author=user,
            category=category,
            title=title,
            content=content,
            image=final_image,
            is_active=is_active,
            tags=[]
        )
        new_post.save()

        # commit tags changes
        tags_changes(tags, new_post)

        # save tags object in post

        new_post.tags = [Tag.objects(name=tag.strip()).first() for tag in tags]
        new_post.save()

        return redirect(url_for('user.post_list'))

    else:
        tags = Tag.objects().limit(6)
        categories = Category.objects()
        tags_str = ''
        for tag in tags:
            tags_str = f"{tags_str}, {tag.name}"
        return render_template('user/create.html', tags=tags_str, categories=categories)


@bp.route('/post-list/')
def post_list():
    """ return user's posts"""
    user = g.user
    user_post = Post.objects(author=user).order_by('-id')
    return render_template('user/post_list.html', posts=user_post)
#
#
# @bp.route('/edit-post/')
# def edit_post():
#     return render_template('edit_post.html', username=None)
