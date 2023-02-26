from wtforms import Form
from wtforms.fields import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Regexp, Email


class GetInformationFrom(Form):
    username = StringField(validators=[
        DataRequired(message='The user account cannot be empty'),
        Regexp(regex=r'^\w{4,20}$', message='The username is in the wrong format'),
    ])


class LoginFrom(GetInformationFrom):
    password = PasswordField(validators=[
        DataRequired(message='The user password cannot be empty'),
        Length(max=255, message='The max length of password is 255')
    ])
    img_code = StringField(validators=[
        DataRequired(message='The random code cannot be empty'),
        Length(min=4, max=4, message='The length of image code must be 4')
    ])
    image_id = StringField(validators=[DataRequired(message='The image id cannot be empty')])


class ChangePasswordFrom(GetInformationFrom):
    password = PasswordField(validators=[
        DataRequired(message='The password cannot be empty'),
        Length(max=255, message='The max length of password is 255')
    ])


class ChangeAdminPasswordForm(ChangePasswordFrom):
    email_code = StringField(validators=[
        DataRequired(message='The email verification code cannot be empty'),
        Length(min=6, max=6, message='The email verification code must be 6 digits long')
    ])


class ChangeUserPasswordForm(ChangePasswordFrom):
    new_password = PasswordField(validators=[
        DataRequired(message='The new password cannot be empty'),
        Length(max=255, message='The max length of new password is 255')
    ])


class ModifyInfoForm(GetInformationFrom):
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
