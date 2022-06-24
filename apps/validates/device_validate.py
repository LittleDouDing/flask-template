from wtforms import Form
from wtforms.fields import StringField, IntegerField
from wtforms.validators import IPAddress, DataRequired, AnyOf, Optional, Length
from . import Config


class AddDeviceAccountForm(Form):
    region = StringField(validators=[
        DataRequired(message='The region cannot be empty'),
        AnyOf(values=Config.region(), message='The entered region is not within the specified range')
    ])
    place = StringField(validators=[
        DataRequired(message='The place cannot be empty'),
        AnyOf(values=Config.places(), message='The entered place is not within the specified range')
    ])
    device_name = StringField(validators=[
        DataRequired(message='The full_name cannot be empty'),
        Length(max=25, message='The max length of region is 25')
    ])
    device_alias = StringField(validators=[
        DataRequired(message='The device alias cannot be empty'),
        Length(max=30, message='The max length of device name is 30')
    ])
    manage_ip = StringField(validators=[
        DataRequired(message='The manage ip cannot be empty'),
        IPAddress(message='The manage ip does not meet the specification')
    ])
    device_type = StringField(validators=[
        Optional(),
        Length(max=15, message='The max length of device type is 15')
    ])
    room_name = StringField(validators=[
        Optional(),
        Length(max=50, message='The max length of room name is 50')
    ])
    manufacture = StringField(validators=[
        Optional(),
        Length(max=50, message='The max length of manufacture is 5')
    ])
    network_level = StringField(validators=[
        Optional(),
        Length(max=15, message='The max length of network level is 15')
    ])
    device_model = StringField(validators=[
        Optional(),
        Length(max=20, message='The max length of device model is 20')
    ])
    remark = StringField(validators=[
        Optional(),
        Length(max=500, message='The max length of remark is 500')
    ])


class DeleteDeviceAccountForm(Form):
    device_id = IntegerField(validators=[DataRequired(message='The device id cannot be empty')])


class ModifyDeviceAccountForm(AddDeviceAccountForm):
    device_id = IntegerField(validators=[DataRequired(message='The device id cannot be empty')])


class SearchDeviceAccountForm(Form):
    region = StringField(validators=[
        Optional(),
        AnyOf(values=Config.region(), message='The entered region is not within the specified range')
    ])
    device_type = StringField(validators=[
        Optional(),
        Length(max=15, message='The max length of device type is 15')
    ])
    device_name = StringField(validators=[
        Optional(),
        Length(max=25, message='The max length of region is 25')
    ])
    device_alias = StringField(validators=[
        Optional(),
        Length(max=30, message='The max length of device name is 30')
    ])
    manage_ip = StringField(validators=[
        Optional(),
        IPAddress(message='The manage ip does not meet the specification')
    ])
    room_name = StringField(validators=[
        Optional(),
        Length(max=50, message='The max length of room name is 50')
    ])
    manufacture = StringField(validators=[
        Optional(),
        Length(max=50, message='The max length of manufacture is 5')
    ])
    place = StringField(validators=[
        Optional(),
        AnyOf(values=Config.places(), message='The entered place is not within the specified range')
    ])
    page = IntegerField(validators=[
        Optional(),
        DataRequired(message='The number of pages must be an integer')
    ])
