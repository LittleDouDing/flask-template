from wtforms import Form, StringField
from wtforms.validators import DataRequired, Regexp


class GetDevicePortForm(Form):
    device_name = StringField(validators=[DataRequired(message='The device name cannot be empty')])
    device_type = StringField(validators=[
        DataRequired(message='The device type cannot be empty'),
        Regexp(regex=r'^(Bras|Switch)$', message='The device type must be Bras or Switch')
    ])


class AddTopologyForm(Form):
    topology = StringField(validators=[DataRequired('The topology cannot be empty')])
