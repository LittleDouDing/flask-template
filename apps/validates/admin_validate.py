from wtforms import Form
from wtforms.fields import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp, Email, Optional


class BaseUserForm(Form):
    username = StringField(validators=[
        DataRequired(message='The user account cannot be empty'),
        Regexp(regex=r'[a-zA-Z0-9]{4,20}', message='The username is in the wrong format'),
        Length(min=4, max=20, message='The length of the user account must be between 4-20')
    ])
    name = StringField(validators=[
        DataRequired(message='The username cannot be empty'),
        Length(min=2, max=30, message='The length of the username must be between 2-30')
    ])
    sex = StringField(validators=[
        DataRequired(message='The user sex cannot be empty'),
        Regexp(regex=r'[1|2]', message='The user gender must be 1 or 2')
    ])
    email = StringField(validators=[
        DataRequired(message='The user email cannot be empty'),
        Email(message='The user email is not a normal email address')
    ])
    phone = StringField(validators=[
        DataRequired(message='The user phone cannot be empty'),
        Regexp(regex=r'1[34578]\d{9}', message='The phone is in the wrong format')
    ])


class AddUserForm(BaseUserForm):
    password = PasswordField(validators=[DataRequired(message='The user password cannot be empty')])
    author = StringField(validators=[
        DataRequired(message='The user author cannot be empty'),
        Regexp(regex='^(check|configure)$', message='The user permissions can only be check or configure')
    ])


class DeleteUserForm(Form):
    username = StringField(validators=[
        DataRequired(message='The user account cannot be empty'),
        Regexp(regex=r'[a-zA-Z0-9]{4,20}', message='The username is in the wrong format'),
        Length(min=4, max=20, message='The length of the user account must be between 4-20')
    ])


class ChangeUserInfoForm(BaseUserForm):
    author = StringField(validators=[
        DataRequired(message='The user author cannot be empty'),
        Regexp(regex=r'^(check|configure)$', message='The user permissions can only be check or configure')
    ])


class ChangeUserPasswordForm(Form):
    username = StringField(validators=[
        DataRequired(message='The user account cannot be empty'),
        Regexp(regex=r'[a-zA-Z0-9]{4,20}', message='The username is in the wrong format'),
        Length(min=4, max=20, message='The length of the user account must be between 4-20')
    ])
    password = PasswordField(validators=[DataRequired(message='The user password cannot be empty')])


class GetAllUserForm(Form):
    page = IntegerField(validators=[
        Optional(),
        DataRequired(message='The number of pages must be an integer')
    ])
    username = StringField(validators=[
        Optional(),
        Regexp(regex=r'[a-zA-Z0-9]{4,20}', message='The username is in the wrong format'),
        Length(min=4, max=20, message='The length of the user account must be between 4-20')
    ])
    name = StringField(validators=[
        Optional(),
        Length(min=2, max=30, message='The length of the username must be between 2-30')
    ])
