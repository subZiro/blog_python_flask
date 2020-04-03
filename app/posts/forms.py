# -*- coding: utf-8 -*-
# формы для создания поста

from wtforms import Form, StringField, TextAreaField, validators


class PostForm(Form):
    title = StringField('Title', validators=[validators.required(), validators.length(4)])
    description = StringField('Description')
    body = TextAreaField('Content', validators=[validators.required()])
    #status =
    #title_image =




"""id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    title_image = db.Column(db.String(60))
    description = db.Column(db.String(280))
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.now())
    status = db.Column(db.Boolean, default=0)"""