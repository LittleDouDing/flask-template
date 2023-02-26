# coding: utf-8
from sqlalchemy import String, Column, Sequence, ForeignKey, Index, Date
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.event import listen
from apps.models import db

Base = declarative_base()
metadata = Base.metadata
session = db.session


class Admin(Base):
    __tablename__ = 'admin'

    username = Column(VARCHAR(20), primary_key=True, comment='管理员账号(OA账号)')
    password = Column(VARCHAR(255), nullable=False, comment='管理员密码')
    name = Column(VARCHAR(30), nullable=False, comment='管理员姓名')
    sex = Column(VARCHAR(2), nullable=False, comment='管理员性别')
    email = Column(VARCHAR(50), nullable=False, unique=True, comment='管理员邮箱')
    phone = Column(VARCHAR(11), nullable=False, unique=True, comment='管理员联系方式')


class User(Base):
    __tablename__ = 'user'

    username = Column(VARCHAR(20), primary_key=True, comment='用户账号(OA账号)')
    password = Column(VARCHAR(255), nullable=False, comment='用户密码')
    author = Column(VARCHAR(10), nullable=False, comment='用户权限(查看、配置)')
    name = Column(VARCHAR(30), nullable=False, comment='用户姓名')
    sex = Column(VARCHAR(2), nullable=False, comment='用户性别')
    email = Column(VARCHAR(50), nullable=False, unique=True, comment='用户邮箱')
    phone = Column(VARCHAR(11), nullable=False, unique=True, comment='用户联系方式')
    department = Column(VARCHAR(20), nullable=False, comment='部门')
