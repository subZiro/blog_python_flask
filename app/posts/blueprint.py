# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import render_template

from models import Post, Tag

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/')
def posts_pages():
    """ страница всех постов"""
    posts = Post.query.order_by(Post.create_time.desc())
    return render_template('posts/index.html', posts=posts)


@posts.route('/<slug>')
def post_detail(slug):
    """ страница поста """
    post = Post.query.filter(Post.slug==slug).first()
    tags = post.tags
    return render_template('posts/post.html', post=post, tags=tags)


@posts.route('/tag/<slug>')
def tag_detail(slug):
    """ страница постов по определенному тегу """
    tag = Tag.query.filter(Tag.tag_slug==slug).first()
    posts = tag.posts.all()
    return render_template('posts/tag.html', posts=posts, tag=tag)
