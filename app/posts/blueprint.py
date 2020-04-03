# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import render_template
from flask import request

from flask import redirect
from flask import url_for

from models import Post, Tag
from app import db
from .forms import PostForm

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create', methods=['POST', 'GET'])
def create_post():
    """ страница создания поста"""
    if request.method == 'POST':
        title = request.form['title']
        # title_image = 'None'
        description = request.form['description']
        body = request.form['body']
        author_id = 1

        try:
            post = Post(title=title, description=description, body=body, author_id=author_id)
            db.session.add(post)
            db.session.commit()
        except:
            print('Error, cant write to db')
        return redirect(url_for('posts.posts_pages'))

    form = PostForm()
    return render_template('posts/create_post.html', form=form)


@posts.route('/')
def posts_pages():
    """ страница всех постов"""
    pages = request.args.get('page')


    posts = Post.query.order_by(Post.create_time.desc())
    return render_template('posts/index.html', posts=posts)


@posts.route('/<slug>')
def post_detail(slug):
    """ страница поста """
    post = Post.query.filter(Post.slug == slug).first()
    tags = post.tags
    return render_template('posts/post.html', post=post, tags=tags)


@posts.route('/tag/<slug>')
def tag_detail(slug):
    """ страница постов по определенному тегу """
    tag = Tag.query.filter(Tag.tag_slug == slug).first()
    posts = tag.posts.all()
    return render_template('posts/tag.html', posts=posts, tag=tag)
