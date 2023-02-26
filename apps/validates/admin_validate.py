from wtforms import Form
from wtforms.fields import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp, Email, Optional, AnyOf
from . import Config


class BaseUserForm(Form):
    username = StringField(validators=[
        DataRequired(message='The user account cannot be empty'),
        Regexp(regex=r'^\w{4,20}$', message='The username is in the wrong format'),
        Length(min=4, max=20, message='The length of the user account must be between 4-20')
    ])
    name = StringField(validators=[
        DataRequired(message='The name cannot be empty'),
        Length(min=2, max=30, message='The length of the name must be between 2-30')
    ])
    sex = StringField(validators=[
        DataRequired(message='The user sex cannot be empty'),
        Regexp(regex=r'^[1|2]$', message='The user gender must be 1 or 2')
    ])
    email = StringField(validators=[
        DataRequired(message='The user email cannot be empty'),
        Email(message='The user email is not a normal email address')
    ])
    phone = StringField(validators=[
        DataRequired(message='The user phone cannot be empty'),
        Regexp(regex=r'^1[34578]\d{9}$', message='The phone is in the wrong format')
    ])
    department = StringField(validators=[
        DataRequired(message='The department cannot be empty'),
        AnyOf(values=Config.department(), message='The entered department is not within the specified range')
    ])


class AddUserForm(BaseUserForm):
    password = PasswordField(validators=[
        DataRequired(message='The user password cannot be empty'),
        Length(min=10, max=255, message='The length of password must in 10 to 255')
    ])
    author = StringField(validators=[
        DataRequired(message='The user author cannot be empty'),
        Regexp(regex='^(check|configure|other)$', message='The user permissions can only be check、configure or other')
    ])


class DeleteUserForm(Form):
    username = StringField(validators=[
        DataRequired(message='The user account cannot be empty'),
        Regexp(regex=r'^\w{4,20}$', message='The username is in the wrong format'),
    ])


class ChangeUserInfoForm(BaseUserForm):
    author = StringField(validators=[
        DataRequired(message='The user author cannot be empty'),
        Regexp(regex=r'^(check|configure|other)$', message='The user permissions can only be check、configure or other')
    ])


class ChangeUserPasswordForm(Form):
    username = StringField(validators=[
        DataRequired(message='The user account cannot be empty'),
        Regexp(regex=r'^\w{4,20}$', message='The username is in the wrong format'),
    ])
    password = PasswordField(validators=[DataRequired(message='The user password cannot be empty')])


class GetAllUserForm(Form):
    page = IntegerField(validators=[
        Optional(),
        DataRequired(message='The number of pages must be an integer')
    ])
    limit = IntegerField(validators=[
        Optional(),
        DataRequired(message='The limit of pages must be an integer')
    ])
    username = StringField(validators=[
        Optional(),
        Regexp(regex=r'^\w{4,20}$', message='The username is in the wrong format'),
    ])
    name = StringField(validators=[
        Optional(),
        Length(min=2, max=30, message='The length of the name must be between 2-30')
    ])
    sex = StringField(validators=[
        Optional(),
        Regexp(regex=r'^[1|2]$', message='The user gender must be 1 or 2')
    ])
    department = StringField(validators=[
        Optional(),
        AnyOf(values=Config.department(), message='The entered department is not within the specified range')
    ])
    author = StringField(validators=[
        Optional(),
        Regexp(regex='^(check|configure|other)$', message='The user permissions can only be check、configure or other')
    ])
