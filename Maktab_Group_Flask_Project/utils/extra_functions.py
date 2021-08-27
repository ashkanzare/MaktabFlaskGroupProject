
from ..models import User, Tag, Category, LikeDislike

from werkzeug.security import generate_password_hash
from flask import request, redirect, url_for, flash, json

from hashlib import sha256
import os


def check_photo(image, _id, dir_name, hash_word, default_photo=''):
    """ make a directory for the user and save photo in it at media/users """
    photo = default_photo
    if image:
        extension = image.filename.split('.')[-1]
        try:
            os.makedirs(f'static/media/{dir_name}s/{dir_name}_{_id}/')
        except FileExistsError:
            pass
        path = f'static/media/{dir_name}s/{dir_name}_{_id}/' + \
               sha256(request.form[hash_word].encode()).hexdigest() + '.' + extension
        image.save(path)
        photo = path[7:]
    return photo


def change_photo(image, post, hash_word):
    """ make a directory for the user and save photo in it at media/users """
    if image:
        path = post.image.split('/')
        extension = image.filename.split('.')[-1]
        path[-1] = sha256(request.form[hash_word].encode()).hexdigest() + '.' + extension
        photo = '/'.join(path)
        image.save(f'static/{photo}')
        return photo
    return post.image


def check_for_register_errors(username, password, re_password, email):
    """ check username and password for not being empty and check if the username is unique in database """
    error = None

    if re_password != password:
        error = 'رمز عبور با تکرار رمز یکسان نیست'

    if not username:
        error = "نام کاربری را وارد کنید"

    elif not password:
        error = "رمز عبور را وارد کنید"

    elif User.objects(username=username).first() is not None:
        error = f" نام کاربری {username} گرفته شده است"

    elif User.objects(email=email).first() is not None:
        error = f" ایمیل {email} گرفته شده است"

    return error


def create_user(user_field, image):
    """ if there is no error then this function will create the user in database """
    new_user = User(
        first_name=user_field['first_name'],
        last_name=user_field['last_name'],
        username=user_field['username'],
        email=user_field['email'],
        photo='',
        password=generate_password_hash(user_field['password']),
    )

    new_user.save()

    # make directory for user profile picture
    photo = check_photo(image, new_user.id, 'user', 'username')
    new_user.photo = photo
    new_user.save()

    flash('ثبت نام شما با موفقیت انجام شد', 'text-success')
    return True


def lower_form_values(request_):
    user_field = {
        'first_name': request_.form['first_name'],
        'last_name': request_.form['last_name'],
        'username': request_.form['username'],
        'email': request_.form['email'],
        'password': request_.form['password'],
        're_password': request_.form['re_password'],

    }
    # lower the fields
    for field in user_field.keys():
        user_field[field] = user_field[field].lower()

    return user_field


def check_user_email_username(username, email, user_id):
    check_user = User.objects(username=username).first()
    check_email = User.objects(email=email).first()

    if check_user and check_user.id != user_id:
        return 'invalid_username'

    elif check_email and check_email.id != user_id:
        return 'invalid_email'

    else:
        return True


def tags_changes(tags, new_post):
    """ check if tag is not exist then create it and if tag exist then add tag to post """
    if tags:
        for tag in tags:
            if not Tag.objects(name=tag.strip()).first():
                new_tag = Tag(name=tag.strip())
                new_tag.save()
                new_tag.update(push__posts=new_post)
                new_tag.save()
            else:
                new_tag = Tag.objects(name=tag.strip()).first()
                if new_post not in new_tag.posts:
                    new_tag.update(push__posts=new_post)
                    new_tag.save()


def find_categories(categories):
    for category in categories:
        have_child = Category.objects(__raw__={"path": {"$regex": fr"^{category['path']}\/[^\/]*$"}})
        if have_child:
            category['children'] = json.loads(have_child.to_json())
            find_categories(category['children'])
    return categories



def set_likes_count(post):
    post.likes_count = LikeDislike.counter(post.id, True)
    post.dislikes_count = LikeDislike.counter(post.id, False)
    post.save()
    return True
