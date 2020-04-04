# -*- coding: utf-8 -*-
# настройки


class Configuration(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:12345678@localhost/flaskblog'
    SECRET_KEY = 'verrrrry secret key'

    # --flask security-- #
    SECURITY_PASSWORD_SALT = 'securitysalt'
    SECURITY_PASSWORD_HASH = 'plaintext'
