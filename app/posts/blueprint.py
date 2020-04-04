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
    """ страница всех постов 6 постов на одной странице"""
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    posts = Post.query.order_by(Post.create_time.desc())  # отображение постов по дате (от нового к старому)
    pages = posts.paginate(page=page, per_page=6)  # пагинация постов по 6 постов на странице
    return render_template('posts/index.html', pages=pages)


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
