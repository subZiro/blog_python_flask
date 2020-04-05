# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import render_template
from flask import request

from flask import redirect
from flask import url_for

from flask_security import login_required


from models import Post, Tag, User
from app import db
from .forms import PostForm

posts = Blueprint('posts', __name__, template_folder='templates')


def f_set_page():
    """функция возвращает номер страницы паганации"""
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    return page


@posts.route('/')
def posts_pages():
    """ страница всех постов 6 постов на одной странице"""
    page = f_set_page()
    posts = Post.query.order_by(Post.create_time.desc())  # отображение постов по дате (от нового к старому)
    pages = posts.paginate(page=page, per_page=6)  # пагинация постов по 6 постов на странице
    return render_template('posts/index.html', pages=pages)


@posts.route('/<slug>/')
def post_detail(slug):
    """ страница поста """
    post = Post.query.filter(Post.slug == slug).first_or_404()
    tags = post.tags
    return render_template('posts/post.html', post=post, tags=tags)


@posts.route('/tag/<slug>/')
def tag_detail(slug):
    """ страница постов по определенному тегу
    посты выводятся с пагинацей по 5 на странице
    порядок от новых к старым"""
    tag = Tag.query.filter(Tag.tag_slug == slug).first_or_404()  # слаг по тегу или 404
    posts = tag.posts.order_by(Post.create_time.desc())  # получение всех постов тега, вывод от нового к старому
    page = f_set_page()
    pages = posts.paginate(page=page, per_page=5)  # пагинация постов по 5 постов на странице
    return render_template('posts/tag.html', pages=pages, tag=tag)


@posts.route('/author/<name>/')
def author_detail(name):
    """ страница постов по определенному автору """
    author = User.query.filter(User.name==name).first_or_404()  # имя автора если такого не существует ошибка
    posts = author.posts.order_by(Post.create_time.desc())  # все посты автора от нового к старому
    page = f_set_page()
    pages = posts.paginate(page=page, per_page=5)  # пагинация постов по 5 постов на странице
    return render_template('posts/author.html', pages=pages, author=author)


@posts.route('/create', methods=['POST', 'GET'])
@login_required
def create_post():
    """ страница создания поста"""
    if request.method == 'POST':
        title = request.form['title']
        # title_image = 'None'
        description = request.form['description']
        body = request.form['body']
        author_id = 1

        try:
            # запись в бд
            post = Post(title=title, description=description, body=body, author_id=author_id)
            db.session.add(post)
            db.session.commit()
        except:
            print('Error, cant write to db')
        return redirect(url_for('posts.posts_pages'))

    form = PostForm()
    return render_template('posts/create_post.html', form=form)


@posts.route('/<slug>/edit', methods=['POST', 'GET'])
@login_required
def edit_post(slug):
    """редактирование поста"""
    post = Post.query.filter(Post.slug==slug).first_or_404()

    if request.method == 'POST':
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()
        return redirect(url_for('posts.post_detail', slug=post.slug))

    form = PostForm(obj=post)
    return render_template('posts/edit_post.html', form=form, post=post)