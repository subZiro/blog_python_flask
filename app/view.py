# -*- coding: utf-8 -*-

from flask import render_template

from app import app

from models import Post


@app.route('/')
@app.route('/index.html')
def index():
    posts = Post.query.filter(Post.status == 1).all()
    return render_template('index.html', posts=posts)


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