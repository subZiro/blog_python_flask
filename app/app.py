# -*- coding: utf-8 -*-
# иниц различных модулей приложения

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask import redirect, url_for, request
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView

from flask_security import SQLAlchemyUserDatastore
from flask_security import Security
from flask_security import current_user


from config import Configuration


# --иниц flask приложения-- #
app = Flask(__name__)

# --настройки-- #
app.config.from_object(Configuration)

# --подключение к бд через sqlalchemy--#
db = SQLAlchemy(app)

# --миграции бд-- #
migrate = Migrate(app, db)

# --менеджер работы с миграциями-- #
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# --подключение админки-- #
from models import *


class AdminMixin:
    def is_accessible(self):
        """переопределение доступности вью конкретному пользователю"""
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        """если вью недоступна пользователю, перенаправляем на страницу авторизации"""
        return redirect(url_for('security.login', next=request.url))


class BaseModelView(ModelView):
    """"""
    def on_model_change(self, form, model, is_created):
        """переопределение метода формы админ панели создания/редактирования"""
        model.generate_slug()
        return super(BaseModelView, self).on_model_change(form, model, is_created)


class PostAdminView(AdminMixin, BaseModelView):
    """клас для отображения постов в админпанели"""
    form_columns = ['title', 'title_image', 'description', 'body', 'tags', 'status']


class TagAdminView(AdminMixin, BaseModelView):
    """клас для отображения тегов в админпанели"""
    form_columns = ['tag_name']


class UserAdminView(AdminMixin, BaseModelView):
    """клас для отображения пользователей в админпанели"""
    form_columns = ['roles', 'name', 'email', 'password', 'active']


class RoleAdminView(AdminMixin, BaseModelView):
    """клас для отображения пользователей в админпанели"""
    form_columns = ['name', 'description']


class AdminView(AdminMixin, ModelView):
    """переопределение вью админки для админов"""
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    """запрет открытия админки не админам"""
    pass


admin = Admin(app, 'Flask App', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(PostAdminView(Post, db.session))
admin.add_view(TagAdminView(Tag, db.session))
admin.add_view(UserAdminView(User, db.session))
admin.add_view(RoleAdminView(Role, db.session))

# --flask security-- #
userdatastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, userdatastore)
