from wtforms import Form, StringField, IntegerField
from wtforms.validators import DataRequired, Regexp, Optional
from wtforms import ValidationError
from . import Config
import re


class GetDevicePortForm(Form):
    device_name = StringField(validators=[DataRequired(message='The device name cannot be empty')])
    device_type = StringField(validators=[
        DataRequired(message='The device type cannot be empty'),
        Regexp(regex=r'^(Bras|Switch)$', message='The device type must be Bras or Switch')
    ])


class GetTopologyForm(Form):
    device_name = StringField(validators=[Optional()])
    page = IntegerField(validators=[
        Optional(),
        DataRequired(message='The number of pages must be an integer')
    ])


class ModifyTopologyForm(Form):
    topology_id = IntegerField(validators=[DataRequired(message='The topology id cannot be empty')])
    topology = StringField(validators=[DataRequired('The topology cannot be empty')])


class AddTopologyForm(Form):
    topology = StringField(validators=[DataRequired('The topology cannot be empty')])

    def validate_topology(self, filed):  # 自定义验证器：validate_字段名
        if not isinstance(filed.data, list):
            raise ValidationError('The data format of the topology is not an array')
        for item in self.topology.data:
            port_regex = re.sub(r'[\^$]', '', Config.port_regex())
            port_regex = r'^.+:' + port_regex + '$'
            if not re.findall(port_regex, item):
                raise ValidationError('The device port ' + item + ' does not conform to the specification')


class DeleteTopologyForm(Form):
    topology_id = IntegerField(validators=[DataRequired(message='The topology id cannot be empty')])
