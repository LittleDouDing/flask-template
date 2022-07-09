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


class AddChangeAccountForm(Form):
    change_time = DateField(validators=[DataRequired(message='The change time cannot be empty')])
    name = StringField(validators=[
        DataRequired(message='The name cannot be empty'),
        Length(max=50, message='The max length of name is 50')
    ])
    start_ip = StringField(validators=[DataRequired(message='The start ip cannot be empty')])
    end_ip = StringField(validators=[DataRequired(message='The end ip cannot be empty')])
    monotony = StringField(validators=[
        DataRequired(message='The monotony cannot be empty'),
        Length(max=30, message='The max length of monotony is 30')
    ])
    product_code = StringField(validators=[
        DataRequired(message='The product code  cannot be empty'),
        Length(max=30, message='The max length of product code  is 30')
    ])
    access_device = StringField(validators=[
        DataRequired(message='The access device cannot be empty'),
        Length(max=25, message='The max length of access device is 25')
    ])
    device_ip = StringField(validators=[
        DataRequired(message='The device ip cannot be empty'),
        IPAddress(message='The device ip does not meet the specification')
    ])
    access_port = StringField(validators=[
        DataRequired(message='The access port cannot be empty'),
        Length(max=30, message='The max length of access port is 30')
    ])
    bandwidth = StringField(validators=[
        DataRequired(message='The bandwidth cannot be empty'),
        Length(max=10, message='The max length of bandwidth is 10')
    ])
    status = StringField(validators=[
        DataRequired(message='The status cannot be empty'),
        Regexp(r'^(0|1)$', message='The status must be 0 or 1')
    ])
    business_type = StringField(validators=[
        DataRequired(message='The business type cannot be empty'),
        Regexp(r'^(IDC|智享专车|商务快车|DIA|楼宇专线)$', message='The business type does not meet the specification')
    ])
    is_close = StringField(validators=[
        DataRequired(message='The closing cannot be empty'),
        Regexp(r'^(0|1)$', message='The closing must be 0 or 1')
    ])

    def validate_start_ip(self, filed):  # 自定义验证器：validate_字段名
        if not isinstance(filed.data, list):
            raise ValidationError('The data format of the ipaddress is not an array')
        for item in self.start_ip.data:
            if not re.match(Config.ipaddress(), item):
                raise ValidationError('The start ip ' + item + ' does not conform to the specification')

    def validate_end_ip(self, filed):  # 自定义验证器：validate_字段名
        if not isinstance(filed.data, list):
            raise ValidationError('The data format of the ipaddress is not an array')
        for item in self.end_ip.data:
            if not re.match(Config.ipaddress(), item):
                raise ValidationError('The start ip ' + item + ' does not conform to the specification')


class GetChangeAccountForm(Form):
    change_time = StringField(validators=[
        Optional(),
        Length(max=10, message='The max length of change time is 10')
    ])
    name = StringField(validators=[
        Optional(),
        Length(max=50, message='The max length of name is 50')
    ])
    product_code = StringField(validators=[
        Optional(),
        Length(max=30, message='The max length of product code  is 30')
    ])
    page = IntegerField(validators=[
        Optional(),
        DataRequired(message='The number of pages must be an integer')
    ])
