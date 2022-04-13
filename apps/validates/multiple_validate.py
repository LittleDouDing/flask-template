from wtforms import StringField, Form
from wtforms.validators import DataRequired, Regexp, AnyOf, Optional, Length
from apps.utils.util_tool import handle_filed
from . import Config


class AddMultipleAccountForm(Form):
    multiple_name = StringField(validators=[
        DataRequired(message='The multiple name cannot be empty'),
        Length(max=30, message='The max length of multiple name is 50')
    ])
    place = StringField(validators=[
        DataRequired(message='The place cannot be empty'),
        AnyOf(values=Config.places(), message='The entered place is not within the specified range')
    ])
    band_vlan = StringField(validators=[
        Optional(),
        Regexp(Config.vlan(), message='The band vlan does not conform to the specification')
    ])
    iptv_vlan = StringField(validators=[
        Optional(),
        Regexp(Config.vlan(), message='The band vlan does not conform to the specification')
    ])
    voice_vlan = StringField(validators=[
        Optional(),
        Regexp(Config.vlan(), message='The band vlan does not conform to the specification')
    ])
    multiple_ip = StringField(DataRequired(message='The multiple ipaddress cannot be empty'))
    manage_vlan = StringField(DataRequired(message='The manage ipaddress cannot be empty'))
    use_way = StringField(DataRequired(message='The use way cannot be empty'))
    topology = StringField(DataRequired(message='The topology cannot be empty'))
    access_information = StringField(DataRequired(message='The access information cannot be empty'))
    relate_devices = StringField(DataRequired(message='The relate devices cannot be empty'))
    remark = StringField(validators=[Optional()])
    monotony = StringField(validators=[Optional()])
    circuit_code = StringField(validators=[Optional()])
    scenes = StringField()
    is_protect = StringField()
    is_room = StringField()

    def validate_multiple_ip(self, filed):  # 自定义验证器：validate_字段名
        handle_filed(filed, 'multiple ip', self.multiple_ip.data, Config.ipaddress())

    def validate_manage_vlan(self, filed):  # 自定义验证器：validate_字段名
        handle_filed(filed, 'manage vlan', self.manage_vlan.data, Config.vlan())

    def validate_use_way(self, filed):  # 自定义验证器：validate_字段名
        handle_filed(filed, 'use way', self.use_way.data, r'^(裸纤|分组)$')

    def validate_topology(self, filed):  # 自定义验证器：validate_字段名
        handle_filed(filed, 'topology', self.topology.data, Config.device_port(), is_topology=True)

    def validate_access_information(self, filed):
        handle_filed(filed, 'access_information', self.access_information.data, Config)
