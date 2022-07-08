#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib import parse
from datetime import timedelta


class Config:
    TESTING = False
    # 配置jwt
    JWT_SECRET_KEY = 'Super_Secret_JWT_KEY'
    JWT_ACCESS_TOKEN_EXPIRES = False
    JWT_REFRESH_TOKEN_EXPIRES = False
    # 配置sqlcharmy
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'ledgersystem'
    USERNAME = 'root'
    PASSWORD = parse.quote_plus('Lin123456@')
    DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=utf8"
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 每次请求结束之后都会提交数据库的变动
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 调试
    SQLALCHEMY_ECHO = False
    # 配置邮箱
    MAIL_SERVER = "smtp.163.com"
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_DEFAULT_SENDER = ('LedgerSystem', 'little_bean2022@163.com')
    MAIL_USERNAME = 'little_bean2022@163.com'
    MAIL_PASSWORD = "UUXYDJQPGBNFSYXM"
    # 文件配置
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    UPLOAD_EXTENSIONS = ['.xls']


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'


class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'


class TestingConfig(Config):
    TESTING = True
