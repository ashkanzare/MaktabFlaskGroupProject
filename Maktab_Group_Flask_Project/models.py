from datetime import datetime

from Maktab_Group_Flask_Project.db import get_db

db = get_db()


# Mongo database model

class User(db.Document):
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    username = db.StringField(max_length=50)
    email = db.StringField(required=False, null=True)
    photo = db.StringField(required=False, null=True)
    password = db.StringField(required=True)
    date = db.DateTimeField(required=True, default=datetime.now())
    bio = db.StringField(default='')

    def __str__(self):
        return self.username


class Category(db.Document):
    name = db.StringField(max_length=30, required=True, unique=True)
    # parent = db.ReferenceField('self', required=False, null=True)
    path = db.StringField(required=True, default='0')

    def __str__(self):
        return self.name


class Post(db.Document):
    author = db.DictField(required=True)
    category = db.ReferenceField(Category, required=True)
    title = db.StringField(max_length=250, required=True)
    content = db.StringField(required=True)
    image = db.StringField(required=False, null=True)
    is_active = db.BooleanField(default=True)
    tags = db.ListField(required=False, null=True)
    likes_count = db.IntField(required=False, default=0)
    dislikes_count = db.IntField(required=False, default=0)
    comments_count = db.IntField(required=False, default=0)
    date = db.DateTimeField(required=True, default=datetime.now())

    def __str__(self):
        return f"{self.author} -- {self.category.name} -- {self.title} -- {self.likes_count}"


class Tag(db.Document):
    name = db.StringField(max_length=30, required=True)
    posts = db.ListField(db.ReferenceField(Post), required=False, reverse_delete_rule=db.CASCADE)

    def __str__(self):
        return self.name


class LikeDislike(db.Document):
    user = db.ReferenceField(User, required=True, reverse_delete_rule=db.CASCADE)
    post = db.ReferenceField(Post, required=True, reverse_delete_rule=db.CASCADE)
    value = db.BooleanField(required=True)

    def __str__(self):
        return f"{self.user} -- {self.post.title} -- {self.value}"

    @classmethod
    def counter(cls, post_id, action):
        return len(cls.objects(post=post_id, value=action))


class Comment(db.Document):
    user = db.DictField(required=True)
    post = db.ReferenceField(Post, required=True, reverse_delete_rule=db.CASCADE)
    comment = db.StringField(required=True)
    date = db.StringField(required=True)

    def __str__(self):
        return f"{self.user} -- {self.post.title} -- {self.comment}"

    @classmethod
    def top_3_comment(cls, post):
        return Comment.objects(post=post).limit(3)

