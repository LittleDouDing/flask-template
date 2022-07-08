from wtforms import StringField, Form, DateField, IntegerField
from wtforms.validators import DataRequired, Regexp, AnyOf, Optional, Length, IPAddress
from wtforms import ValidationError
import re
from . import Config


class AddNetworkAccountForm(Form):
    place = StringField(validators=[
        DataRequired(message='The place cannot be empty'),
        AnyOf(values=Config.places(), message='The entered place is not within the specified range')
    ])
    name = StringField(validators=[
        DataRequired(message='The customer name cannot be empty'),
        Length(max=50, message='The max length of name is 50')
    ])
    vlan = StringField(validators=[
        Optional(),
        Length(max=10, message='The max length of vlan is 10')
    ])
    ip_address = StringField(validators=[DataRequired(message='The ipaddress cannot be empty')])
    mask_router_dns = StringField(validators=[DataRequired(message='The mask and router and dns cannot be empty')])
    sub_interface = StringField(validators=[
        Optional(),
        Regexp(regex=r'^(\d+|\d+/\d+)$', message='The sub interface does not conform to the specification')
    ])
    topology = StringField(validators=[DataRequired(message='The topology cannot be empty')])
    access_information = StringField(validators=[Optional()])
    relate_device = StringField(validators=[DataRequired(message='The relate device cannot be empty')])
    bandwidth = StringField(validators=[
        Optional(),
        Regexp(regex=r'^(\d+M|\d+M/\d+M)$', message='The end bandwidth does not conform to the specification')
    ])
    business_type = StringField(validators=[
        Optional(),
        Length(max=10, message='The max length of business type is 10')
    ])
    user_address = StringField(validators=[
        Optional(),
        Length(max=200, message='The max length of user address is 200')
    ])
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
    remark = StringField(validators=[
        Optional(),
        Length(max=500, message='The max length of remark is 500')
    ])
    finnish_time = DateField(validators=[Optional()])
    product_code = StringField(validators=[
        Optional(),
        Length(max=30, message='The max length of product code is 30')
    ])
    monotony = StringField(validators=[
        Optional(),
        Length(max=30, message='The max length of monotony is 30')
    ])
    circuit_code = StringField(validators=[
        Optional(),
        Length(max=30, message='The max length of circuit code is 30')
    ])
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

    def validate_topology(self, filed):  # 自定义验证器：validate_字段名
        if not isinstance(filed.data, list):
            raise ValidationError('The data format of the topology is not an array')
        for item in self.topology.data:
            if str(item).count(':') != 1:
                raise ValidationError('The topology ' + item + ' does not conform to the specification')

    def validate_access_information(self, filed):  # 自定义验证器：validate_字段名
        if not isinstance(filed.data, list):
            raise ValidationError('The data format of the access information is not an array')
        for item in self.access_information.data:
            if str(item).count(':') != 1:
                raise ValidationError('The access information ' + item + ' does not conform to the specification')

    def validate_relate_device(self, filed):  # 自定义验证器：validate_字段名
        if not isinstance(filed.data, list):
            raise ValidationError('The data format of the relate device is not an array')
        for item in self.relate_device.data:
            if str(item).count('：') != 1:
                raise ValidationError('The relate device ' + item + ' does not conform to the specification')


class DeleteNetworkAccountForm(Form):
    network_id = StringField(validators=[DataRequired(message='The network id cannot be empty')])


class ModifyNetworkAccountForm(AddNetworkAccountForm):
    network_id = StringField(validators=[DataRequired(message='The network id cannot be empty')])


class GetNetworkAccountForm(Form):
    place = StringField(validators=[
        Optional(),
        AnyOf(values=Config.places(), message='The entered place is not within the specified range')
    ])
    name = StringField(validators=[
        Optional(),
        Length(max=50, message='The max length of name is 50')
    ])
    vlan = StringField(validators=[
        Optional(),
        Length(max=10, message='The max length of vlan is 10')
    ])
    ip_address = StringField(validators=[
        Optional(),
        IPAddress(message='The main ipaddress does not meet the specification')
    ])
    sub_interface = StringField(validators=[
        Optional(),
        Regexp(regex=r'^(\d+|\d+/\d+)$', message='The sub interface does not conform to the specification')
    ])
    topology = StringField(validators=[
        Optional(),
        Length(max=20, message='The max length of topology is 20')
    ])
    access_information = StringField(validators=[
        Optional(),
        Length(max=20, message='The max length of access information is 20')
    ])
    business_type = StringField(validators=[
        Optional(),
        Length(max=10, message='The max length of business type is 10')
    ])
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
    product_code = StringField(validators=[
        Optional(),
        Length(max=30, message='The max length of product code is 30')
    ])
    monotony = StringField(validators=[
        Optional(),
        Length(max=30, message='The max length of monotony is 30')
    ])
    circuit_code = StringField(validators=[
        Optional(),
        Length(max=30, message='The max length of circuit code is 30')
    ])
    is_open = StringField(validators=[
        Optional(),
        Regexp(regex=r'^(0|1)$', message='The 80 port must be 0 or 1')
    ])
    page = IntegerField(validators=[
        Optional(),
        DataRequired(message='The number of pages must be an integer')
    ])
