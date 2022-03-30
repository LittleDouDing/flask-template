from wtforms import Form
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Regexp, Email, Optional


class GetInformationFrom(Form):
    username = StringField(validators=[
        DataRequired(message='The user account cannot be empty'),
        Length(min=4, max=20, message='The length of the user account must be between 4-20')
    ])


class LoginFrom(GetInformationFrom):
    password = PasswordField(validators=[DataRequired(message='The user password cannot be empty')])


class ChangePasswordFrom(GetInformationFrom):
    password = PasswordField(validators=[DataRequired(message='The password cannot be empty')])


class ChangeAdminPasswordForm(ChangePasswordFrom):
    email_code = StringField(validators=[
        DataRequired(message='The email verification code cannot be empty'),
        Length(min=6, max=6, message='The email verification code must be 6 digits long')
    ])


class ChangeUserPasswordForm(ChangePasswordFrom):
    new_password = PasswordField(validators=[DataRequired(message='The new password cannot be empty')])


class ModifyInfoForm(GetInformationFrom):
    name = StringField(validators=[
        Optional(),
        Length(min=2, max=30, message='The length of the username must be between 2-30')
    ])
    sex = StringField(validators=[
        Optional(),
        Regexp(regex=r'[1|2]', message='The user gender must be 1 or 2')
    ])
    email = StringField(validators=[
        Optional(),
        Email(message='The user email is not a normal email address')
    ])
    phone = StringField(validators=[
        Optional(),
        Regexp(regex=r'1[34578]\d{9}', message='wrong phone number format')
    ])
