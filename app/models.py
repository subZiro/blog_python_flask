# -*- coding: utf-8 -*-
# работа с моделями бд

import os
import re
from datetime import datetime

from app import db

post_tags = db.Table('post_tags',
                     db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                     )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    is_admin = db.Column(db.Integer, default=0)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        """инициализация"""
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        """представление класса в консоли"""
        return f'<User id: {self.id}, name:{self.name}>'


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(100))
    tag_slug = db.Column(db.String(100))

    def __init__(self, *args, **kwargs):
        """инициализация"""
        super(Tag, self).__init__(*args, **kwargs)
        self.tag_slug = f_slugify(self.tag_name)

    def __repr__(self):
        """представление класса в консоли"""
        return f'<Tag id: {self.id}, name:{self.tag_name}>'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    title_image = db.Column(db.String(60))
    description = db.Column(db.String(280))
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())
    status = db.Column(db.Boolean, default=0)

    def __init__(self, *args, **kwargs):
        """инициализация"""
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()

    def __repr__(self):
        """представление класса в консоли"""
        return f'<Post id: {self.id}, title:{self.title}>'

    tags = db.relationship('Tag',
                           secondary=post_tags,
                           backref=db.backref('posts', lazy='dynamic')
                           )

    def generate_slug(self):
        """создание слага"""
        if self.title:
            self.slug = f_slugify(self.title)

    def get_description(self):
        """получение описания если оно существует"""
        if self.description:
            return self.description
        else:
            return ''


    def get_author(self):
        """временное решение возврат псевдонима админа"""
        a = {1: 'Start Flask', 2: 'I AM', 3: 'CatDog', 4: 'AKIRA'}
        if not self.author_id:
            return 'Administrator'
        return self.author.name

    def get_formated_date(self, format='%B %d, %Y'):
        """получение даты в формате d mounth YYYY"""
        if not self.create_time:
            return ''
        else:
            return self.create_time.strftime(format)

    def get_title_image(self):
        """получение изображения для заголовка поста, если изображение отсутствует то грузить default"""
        if not self.title_image:
            return 'img/no-title-image.jpg'
        return self.title_image


def f_slugify(s: str):
    """генерация валидного url из строки"""
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s.lower())


def upload_folder(workspace='/static/img', folder='upload'):
    """если папки не существует создание папки upload
    create_folder(r"C:\TEMP\person\age1", "Gulag")
    create folder with path C:\TEMP\person\age1\Gulag"""
    path = os.path.join(workspace, folder)
    if not os.path.exists(path):
        os.makedirs(path)
        print("create folder with path {0}".format(path))
    else:
        print("folder exists {0}".format(path))
