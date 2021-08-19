from flask import render_template, request, redirect, url_for, flash, Blueprint
from Maktab_Group_Flask_Project.models import User, Tag, Category, Post
from flask import g
from werkzeug.security import generate_password_hash

import os
from hashlib import sha256

bp = Blueprint("user", __name__)


# bakhshe profile va post-list va ejade posts

@bp.route('/profile/')
def profile():
    return render_template('user/profile.html', user=g.user)


@bp.route('/edit-profile/', methods=['POST', 'GET'])
def edit_profile():
    if request.method == 'POST':
        user_id = g.user.id
        user = User.objects(id=user_id).first()
        path = user.photo.split('/')
        image = request.files['file']
        ext = image.filename.split('.')[-1]
        photo = user.photo

        if image:
            path = f'static/media/users/{path[2]}/' + \
                   sha256(request.form['username'].encode()).hexdigest() + '.' + ext
            image.save(path)
            photo = path[7:]

        password = request.form['password'].lower()
        re_password = request.form['re_password'].lower()
        if re_password != password:
            flash('The password confirmation does not match')
            return redirect(url_for('user.edit_profile'))
        user.first_name = request.form['first_name'].lower()
        user.last_name = request.form['last_name'].lower()
        check_user = User.objects(username=request.form['username'].lower()).first()
        if check_user:
            if check_user.id != user.id:
                flash('The username already exist')
                return redirect(url_for('user.edit_profile'))
        check_email = User.objects(email=request.form['email'].lower()).first()
        if check_email:
            if check_email.id != user.id:
                flash('The email already taken')
                return redirect(url_for('user.edit_profile'))
        user.username = request.form['username'].lower()
        user.email = request.form['email'].lower()
        user.phone = request.form['email'].lower()
        user.photo = photo
        if password != '' and re_password != '':
            user.password = generate_password_hash(password)
        user.save()
        return render_template('user/profile.html', user=user)
    return render_template('user/edit_profile.html')


@bp.route('/<variable>/delete_post/')
def delete_post(variable):
    post = Post.objects(id=variable).first()
    if post:
        Tag.objects(posts=post).update(pull__posts=post)
        post.delete()
    return redirect(url_for('user.post_list'))


@bp.route('/create-post/', methods=['POST', 'GET'])
def create_post():
    if request.method == 'POST':
        try:
            check_active_exist = request.form['is_active']
            is_active = True
        except:
            is_active = False
        tags = []
        if request.form['invisible']:
            tags = request.form['invisible'].split(',')

        user = g.user
        title = request.form['title']
        content = request.form['content']
        image = request.files['file']
        ext = image.filename.split('.')[-1]
        category_name = request.form['category']
        category = Category.objects(name=category_name.strip()).first()
        final_image = ''
        posts_len = Post.objects().count()
        if image:
            try:
                os.makedirs(f'static/media/posts/post_{posts_len + 1}/')
            except FileExistsError:
                pass
            path = f'static/media/posts/post_{posts_len + 1}/' + \
                   sha256(request.form['title'].encode()).hexdigest() + '.' + ext
            image.save(path)
            final_image = path[7:]
        new_post = Post(
            author=user,
            category=category,
            title=title,
            content=content,
            image=final_image,
            is_active=is_active,
            tags=tags
        )
        new_post.save()
        if tags:
            for i in tags:
                if not Tag.objects(name=i.strip()).first():
                    new_tag = Tag(name=i.strip())
                    new_tag.save()
                    new_tag.update(push__posts=new_post)
                    new_tag.save()
                else:
                    new_tag = Tag.objects(name=i.strip()).first()
                    new_tag.update(push__posts=new_post)
                    new_tag.save()
        return redirect(url_for('user.post_list'))
    else:
        c1 = Category(name='first')
        c1.save()
        tags = Tag.objects().limit(6)
        categories = Category.objects()
        tags_str = ''
        for tag in tags:
            tags_str = f"{tags_str}, {tag.name}"
        return render_template('user/create.html', tags=tags_str, categories=categories)


@bp.route('/post-list/')
def post_list():
    user = g.user
    user_post = Post.objects(author=user)
    return render_template('user/post_list.html', posts=user_post)


@bp.route('/<variable>/edit_post/',methods=['POST', 'GET'])
def edit_post(variable):
    post = Post.objects(id=variable).first()
    user = g.user

    if request.method == 'POST':
        try:
            check_active_exist = request.form['is_active']
            is_active = True
        except:
            is_active = False
        tags = []
        if request.form['invisible']:
            tags = request.form['invisible'].split(',')
        post.title = request.form['title']
        category_name = request.form['category']
        post.category = Category.objects(name=category_name.strip()).first()
        if request.files['file']:
            post.image = request.files['file']
            ext = post.image.filename.split('.')[-1]
            final_image = ''
            posts_len = Post.objects().count()
            if post.image:
                try:
                    os.makedirs(f'static/media/posts/post_{posts_len + 1}/')
                except FileExistsError:
                    pass
                path = f'static/media/posts/post_{posts_len + 1}/' + \
                       sha256(request.form['title'].encode()).hexdigest() + '.' + ext
                post.image.save(path)
                final_image = path[7:]
                post.image = final_image

            else:
                post.image = post.image

        post.content = request.form['content']


        post.save()
        if tags:
            for i in tags:
                if not Tag.objects(name=i.strip()).first():
                    c_tag = Tag(name=i.strip())
                    c_tag.save()
                    c_tag.update(push__posts=post)
                    c_tag.save()
                else:
                    c_tag = Tag.objects(name=i.strip()).first()
                    c_tag.update(push__posts=post)
                    c_tag.save()
        return redirect(url_for('user.post_list'))
    else:
        tags = Tag.objects().limit(6)
        categories = Category.objects()
        tags_str = ''
        for tag in tags:
            tags_str = f"{tags_str}, {tag.name}"
    return render_template('user/edit_post.html', post=post, tags=tags_str, categories=categories )
