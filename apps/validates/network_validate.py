from wtforms import StringField, Form, DateField
from wtforms.validators import DataRequired, Regexp, AnyOf, Optional, Length
from wtforms import ValidationError
import re
from . import Config


class AddNetworkAccountForm(Form):
    place = StringField(validators=[
        DataRequired(message='The place cannot be empty'),
        AnyOf(values=Config.places(), message='The entered place is not within the specified range')
    ])
    name = StringField(validators=[DataRequired(message='The customer name cannot be empty')])
    vlan = StringField(validators=[Optional()])
    ip_address = StringField(validators=[DataRequired(message='The ipaddress cannot be empty')])
    mask_router_dns = StringField(validators=[DataRequired(message='The mask and router and dns cannot be empty')])
    sub_interface = StringField(validators=[
        Optional(),
        Regexp(regex=r'^(\d+|\d+/\d+)$', message='The sub interface does not conform to the specification')
    ])
    topology = StringField(DataRequired(message='The topology cannot be empty'))
    access_information = StringField(validators=[Optional()])
    relate_device = StringField(validators=[DataRequired(message='The relate device cannot be empty')])
    bandwidth = StringField(validators=[
        Optional(),
        Regexp(regex=r'^(\d+M|\d+M/\d+M)$', message='The end bandwidth does not conform to the specification')
    ])
    business_type = StringField(validators=[Optional()])
    user_address = StringField(validators=[Optional()])
    username = StringField(validators=[
        Optional(),
        Length(min=4, max=20, message='The length of the user name must be between 4-20')
    ])
    user_phone = StringField(validators=[
        Optional(),
        Regexp(regex=r'^1[34578]\d{9}$', message='The phone is in the wrong format')
    ])
    user_manager = StringField(validators=[
        Optional(),
        Length(min=4, max=20, message='The length of the user manager must be between 4-20')
    ])
    manager_phone = StringField(validators=[
        Optional(),
        Regexp(regex=r'^1[34578]\d{9}$', message='The phone is in the wrong format')
    ])
    remark = StringField(validators=[Optional()])
    finnish_time = StringField(validators=[
        Optional(),
        # Regexp(regex=r'^202[2-9]/(0[1-9]|1[0-2])/(0[1-9]|[1-2][0-9]|3[0-1])$')
    ])
    product_code = StringField(validators=[Optional()])
    monotony = StringField(validators=[Optional()])
    circuit_code = StringField(validators=[Optional()])
    is_open = StringField(validators=[
        DataRequired(message='The 80 port cannot be empty'),
        Regexp(regex=r'^(0|1)$', message='The 80 port must be 0 or 1')
    ])

    def validate_ip_address(self, filed):  # 自定义验证器：validate_字段名
        if not isinstance(filed.data, list):
            raise ValidationError('The data format of the ipaddress is not an array')
        for item in self.ip_address.data:
            if not re.match(Config.ipaddress(), item):
                raise ValidationError('The ipaddress ' + item + ' does not conform to the specification')

    def validate_mask_router_dns(self, filed):  # 自定义验证器：validate_字段名
        if not isinstance(filed.data, list):
            raise ValidationError('The data format of the mask and router and dns is not an array')
        for item in self.mask_router_dns.data:
            if not re.match(Config.route_regex(), item):
                raise ValidationError('The ipaddress ' + item + ' does not conform to the specification')
