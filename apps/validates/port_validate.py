from wtforms import Form, StringField, IntegerField
from wtforms.validators import Regexp, DataRequired, Optional, Length


class GetPortForm(Form):
    device_name = StringField(validators=[
        Optional(),
        Length(max=30, message='The max length of device name is 30')
    ])
    full_name = StringField(validators=[
        Optional(),
        Regexp(regex=r'^(b\d-[a-z]-gdzj-[a-z]+|r\d-[a-z]-gdzj-[a-z]+|s\d-[a-z]-gdzj-[a-z]+)$',
               message='The device full name does not conform to specification')
    ])
    device_type = StringField(validators=[
        Optional(),
        Regexp(regex=r'^(Bras|Switch)$', message='The device type must be Bras or Switch')
    ])
    page = IntegerField(validators=[
        Optional(),
        DataRequired(message='The number of pages must be an integer')
    ])


class DeletePortForm(Form):
    port_id = IntegerField(validators=[
        DataRequired(message='The port id cannot be empty'),
        Length(max=6, message='The max length of device id is 6')
    ])
