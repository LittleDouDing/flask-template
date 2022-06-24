from wtforms import Form, StringField, IntegerField
from wtforms.validators import DataRequired, Optional, Length, IPAddress, AnyOf
from apps.validates import Config


class AddPortForm(Form):
    device_name = StringField(validators=[
        DataRequired(message='The device name can not be empty'),
        Length(max=30, message='The max length of device name is 30')
    ])
    device_alias = StringField(validators=[
        DataRequired(message='The device name can not be empty'),
        Length(max=30, message='The max length of device alias is 30')
    ])
    manage_ip = StringField(validators=[
        DataRequired(message='The manage ip can not be empty'),
        IPAddress(message='The manage ip does not meet the specification')
    ])
    region = StringField(validators=[
        DataRequired(message='The region can not be empty'),
        AnyOf(values=Config.region(), message='The entered region is not within the specified range')
    ])
    port_bandwidth = StringField(validators=[
        DataRequired(message='The port bandwidth can not be empty'),
        Length(max=5, message='The max length of port bandwidth is 5')
    ])
    port = StringField(validators=[
        DataRequired(message='The port can not be empty'),
        Length(max=30, message='The max length of port is 30')
    ])
    describe = StringField(validators=[
        Optional(),
        Length(max=100, message='The max length of describe is 100')
    ])


class GetPortForm(Form):
    device_name = StringField(validators=[
        Optional(),
        Length(max=30, message='The max length of device name is 30')
    ])
    device_alias = StringField(validators=[
        Optional(),
        Length(max=30, message='The max length of device alias is 30')
    ])
    region = StringField(validators=[
        Optional(),
        AnyOf(values=Config.region(), message='The entered region is not within the specified range')
    ])
    manage_ip = StringField(validators=[
        Optional(),
        IPAddress(message='The manage ip does not meet the specification')
    ])
    port_bandwidth = StringField(validators=[
        Optional(),
        Length(max=5, message='The max length of port bandwidth is 5')
    ])
    page = IntegerField(validators=[
        Optional(),
        DataRequired(message='The number of pages must be an integer')
    ])


class ModifyPortForm(AddPortForm):
    port_id = IntegerField(validators=[DataRequired(message='The port id cannot be empty')])


class DeletePortForm(Form):
    port_id = IntegerField(validators=[DataRequired(message='The port id cannot be empty')])
