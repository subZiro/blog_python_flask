# -*- coding: utf-8 -*-

from flask import render_template
from flask import request

from app import app

from models import Post


@app.route('/')
@app.route('/index.html')
def index():
    """главная страница с пагинацией постов по 4 поста на странице"""
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    posts_s = Post.query.filter(Post.status == 1)  # посты со статусом 1
    posts = posts_s.order_by(Post.create_time.desc())  # отображение постов по дате (от нового к старому)
    pages = posts.paginate(page=page, per_page=4)  # пагинация по 4 поста на странице
    return render_template('index.html', pages=pages)


@app.route('/about.html')
def about_page():
    about = "Lorem ipsum dolor sit amet, consectetur adipisicing elit. " \
            "Saepe nostrum ullam eveniet pariatur voluptates odit, " \
            "fuga atque ea nobis sit soluta odio, adipisci quas excepturi " \
            "maxime quae totam ducimus consectetur?"
    return render_template('about.html', about=about)


@app.route('/contact.html')
def contact_page():
    return render_template('contact.html')


@app.route('/post.html')
def post_page():
    return render_template('post.html')