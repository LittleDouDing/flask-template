from wtforms import StringField, Form, DateField, IntegerField
from wtforms.validators import DataRequired, AnyOf, Optional, Length, IPAddress, Regexp
from wtforms import ValidationError
from . import Config


class AddMultipleAccountForm(Form):
    place = StringField(validators=[
        DataRequired(message='The place cannot be empty'),
        AnyOf(values=Config.places(), message='The entered place is not within the specified range')
    ])
    multiple_name = StringField(validators=[
        DataRequired(message='The multiple name cannot be empty'),
        Length(max=30, message='The max length of multiple name is 50')
    ])
    band_vlan = StringField(validators=[
        Optional(),
        Length(max=20, message='The max length of band vlan is 20')
    ])
    iptv_vlan = StringField(validators=[
        Optional(),
        Length(max=4, message='The max length of iptv vlan is 4')
    ])
    voice_vlan = StringField(validators=[
        Optional(),
        Length(max=4, message='The max length of voice vlan is 4')
    ])
    main_vlan = StringField(validators=[
        DataRequired(message='The main vlan cannot be empty'),
        Length(max=4, message='The max length of main vlan is 4')
    ])
    main_ip = StringField(validators=[
        DataRequired(message='The main manage ip cannot be empty'),
        IPAddress(message='The main manage ip does not meet the specification')
    ])
    main_way = StringField(validators=[
        DataRequired(message='The main way cannot be empty'),
        Length(max=6, message='The max length of main way is 6')
    ])
    main_topology = StringField(validators=[
        DataRequired(message='The main topology cannot be empty'),
        Length(max=500, message='The max length of main topology is 500')
    ])
    main_access = StringField(validators=[
        DataRequired(message='The main access information cannot be empty'),
        Length(max=255, message='The max length of main access information is 255')
    ])
    main_devices = StringField(validators=[
        DataRequired(message='The main relate devices cannot be empty'),
        Length(max=100, message='The max length of main devices is 100')
    ])
    backup_ip = StringField(validators=[
        Optional(),
        IPAddress(message='The backup manage ip does not meet the specification')
    ])
    backup_vlan = StringField(validators=[
        Optional(),
        Length(max=4, message='The max length of backup vlan is 4')
    ])
    backup_way = StringField(validators=[
        Optional(),
        Length(max=6, message='The max length of backup way is 6')
    ])
    backup_topology = StringField(validators=[
        Optional(),
        Length(max=500, message='The max length of backup topology is 500')
    ])
    backup_access = StringField(validators=[
        Optional(),
        Length(max=255, message='The max length of backup access information is 255')
    ])
    backup_devices = StringField(validators=[
        Optional(),
        Length(max=100, message='The max length of backup devices is 100')
    ])
    switch_way = StringField(validators=[
        Optional(),
        Length(max=10, message='The max length of switch way is 10')
    ])
    remark = StringField(validators=[
        Optional(),
        Length(max=500, message='The max length of remark is 500')
    ])
    monotony = StringField(validators=[
        Optional(),
        Length(max=30, message='The max length of monotony is 30')
    ])
    circuit_code = StringField(validators=[
        Optional(),
        Length(max=30, message='The max length of circuit code is 30')
    ])
    scenes = StringField(validators=[
        DataRequired(message='The scenes cannot be empty'),
        Length(max=5, message='The max length of scenes is 5')
    ])
    is_protect = StringField(validators=[
        Optional(),
        Regexp(regex=r'^[0|1]$', message='The protection must be 0 or 1'),
        Length(max=2, message='The max length of protection is 2')
    ])
    is_room = StringField(validators=[
        Optional(),
        Regexp(regex=r'^[0|1]$', message='The room must be 0 or 1'),
        Length(max=2, message='The max length of room is 2')
    ])
    device_name = StringField(validators=[
        DataRequired(message='The device name cannot be empty'),
        Length(max=30, message='The length of device name is 30')
    ])
    longitude_latitude = StringField(validators=[
        Optional(),
        Length(max=20, message='The max length of longitude and latitude is 20')
    ])
    open_time = DateField(validators=[Optional()])

    def validate_main_topology(self, filed):  # 自定义验证器：validate_字段名
        if not isinstance(filed.data, list):
            raise ValidationError('The data format of the main topology is not an array')
        for item in self.main_topology.data:
            if str(item).count(':') != 1:
                raise ValidationError('The main topology ' + item + ' does not conform to the specification')

    def validate_main_access(self, filed):  # 自定义验证器：validate_字段名
        if not isinstance(filed.data, list):
            raise ValidationError('The data format of the main access is not an array')
        for item in self.main_access.data:
            if str(item).count(':') != 1:
                raise ValidationError('The main access ' + item + ' does not conform to the specification')

    def validate_main_devices(self, filed):  # 自定义验证器：validate_字段名
        if not isinstance(filed.data, list):
            raise ValidationError('The data format of the main device is not an array')
        for item in self.main_devices.data:
            if str(item).count('：') != 1:
                raise ValidationError('The main device ' + item + ' does not conform to the specification')

    def validate_backup_topology(self, filed):  # 自定义验证器：validate_字段名
        if not isinstance(filed.data, list):
            raise ValidationError('The data format of the backup topology is not an array')
        for item in self.backup_topology.data:
            if ':' not in item:
                raise ValidationError('The backup topology ' + item + ' does not conform to the specification')

    def validate_backup_access(self, filed):  # 自定义验证器：validate_字段名
        if not isinstance(filed.data, list):
            raise ValidationError('The data format of the backup access is not an array')
        for item in self.backup_access.data:
            if ':' not in item:
                raise ValidationError('The backup access ' + item + ' does not conform to the specification')

    def validate_backup_devices(self, filed):  # 自定义验证器：validate_字段名
        if not isinstance(filed.data, list):
            raise ValidationError('The data format of the backup device is not an array')
        for item in self.backup_devices.data:
            if '：' not in item:
                raise ValidationError('The backup device ' + item + ' does not conform to the specification')


class ModifyMultipleAccountForm(AddMultipleAccountForm):
    multiple_id = StringField(validators=[DataRequired(message='The multiple id cannot be empty')])


class ModifySomeMultipleAccountForm(Form):
    multiple_id = StringField(validators=[DataRequired(message='The multiple id cannot be empty')])
    scenes = StringField(validators=[
        DataRequired(message='The scenes cannot be empty'),
        Length(max=5, message='The max length of scenes is 5')
    ])
    is_room = StringField(validators=[
        Optional(),
        Regexp(regex=r'^[0|1]$', message='The room must be 0 or 1'),
        Length(max=2, message='The max length of room is 2')
    ])
    longitude_latitude = StringField(validators=[
        Optional(),
        Length(max=20, message='The max length of longitude and latitude is 20')
    ])


class DeleteMultipleAccountForm(Form):
    multiple_id = StringField(validators=[DataRequired(message='The multiple id cannot be empty')])


class GetMultipleAccountForm(Form):
    place = StringField(validators=[
        Optional(),
        AnyOf(values=Config.places(), message='The entered place is not within the specified range')
    ])
    multiple_name = StringField(validators=[
        Optional(),
        Length(max=30, message='The max length of multiple name is 50')
    ])
    main_ip = StringField(validators=[
        Optional(),
        IPAddress(message='The main manage ip does not meet the specification')
    ])
    main_way = StringField(validators=[
        Optional(),
        Length(max=6, message='The max length of main way is 6')
    ])
    backup_ip = StringField(validators=[
        Optional(),
        IPAddress(message='The backup manage ip does not meet the specification')
    ])
    switch_way = StringField(validators=[
        Optional(),
        Length(max=10, message='The max length of switch way is 10')
    ])
    monotony = StringField(validators=[
        Optional(),
        Length(max=30, message='The max length of monotony is 30')
    ])
    circuit_code = StringField(validators=[
        Optional(),
        Length(max=30, message='The max length of circuit code is 30')
    ])
    scenes = StringField(validators=[
        Optional(),
        Length(max=5, message='The max length of scenes is 5')
    ])
    is_protect = StringField(validators=[
        Optional(),
        Regexp(regex=r'^[0|1]$', message='The protection must be 0 or 1'),
        Length(max=2, message='The max length of protect is 2')
    ])
    is_room = StringField(validators=[
        Optional(),
        Regexp(regex=r'^[0|1]$', message='The room must be 0 or 1'),
        Length(max=2, message='The max length of room is 2')
    ])
    open_time = DateField(validators=[Optional()])
    page = IntegerField(validators=[
        Optional(),
        DataRequired(message='The number of pages must be an integer')
    ])
