# coding: utf-8
from sqlalchemy import String, Column, Sequence, ForeignKey, Index, Date
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.event import listen
from apps.models import db

Base = declarative_base()
metadata = Base.metadata
session = db.session


class Admin(Base):
    __tablename__ = 'admin'

    username = Column(VARCHAR(20), primary_key=True, comment='管理员账号(OA账号)')
    password = Column(VARCHAR(255), nullable=False, comment='管理员密码')
    name = Column(VARCHAR(30), nullable=False, comment='管理员姓名')
    sex = Column(VARCHAR(2), nullable=False, comment='管理员性别')
    email = Column(VARCHAR(50), nullable=False, unique=True, comment='管理员邮箱')
    phone = Column(VARCHAR(11), nullable=False, unique=True, comment='管理员联系方式')


class User(Base):
    __tablename__ = 'user'

    username = Column(VARCHAR(20), primary_key=True, comment='用户账号(OA账号)')
    password = Column(VARCHAR(255), nullable=False, comment='用户密码')
    author = Column(VARCHAR(10), nullable=False, comment='用户权限(查看、配置)')
    name = Column(VARCHAR(30), nullable=False, comment='用户姓名')
    sex = Column(VARCHAR(2), nullable=False, comment='用户性别')
    email = Column(VARCHAR(50), nullable=False, unique=True, comment='用户邮箱')
    phone = Column(VARCHAR(11), nullable=False, unique=True, comment='用户联系方式')


class DeviceTopology(Base):
    __tablename__ = 'device_topology'

    topology_id = Column(INTEGER(6), Sequence('topology_id_seq'), primary_key=True, comment='设备拓扑id')
    topology = Column(String(500), nullable=False, unique=True, comment='交换机拓扑')


class MultipleAccount(Base):
    __tablename__ = 'multiple_account'

    __table_args__ = (
        Index('place_vlan', 'place', 'band_vlan', 'iptv_vlan', 'voice_vlan', unique=True),
    )

    multiple_id = Column(INTEGER(6), Sequence('multiple_account_id_seq'), primary_key=True, comment='多元化id')
    place = Column(VARCHAR(8), nullable=False, comment='所属区域')
    multiple_name = Column(VARCHAR(50), nullable=False, unique=True, comment='多元化名称')
    band_vlan = Column(VARCHAR(20), comment='宽带vlan')
    iptv_vlan = Column(VARCHAR(4), comment='IPTV vlan')
    voice_vlan = Column(VARCHAR(4), comment='语音vlan')
    main_vlan = Column(String(4), nullable=False, comment='主用网管vlan')
    main_ip = Column(String(15), nullable=False, unique=True, comment='主用登录ip')
    main_way = Column(VARCHAR(6), nullable=False, comment='主用方式')
    main_topology = Column(ForeignKey('device_topology.topology', ondelete='SET NULL', onupdate='CASCADE'), index=True,
                           nullable=False, comment='主用拓扑')
    main_access = Column(VARCHAR(255), nullable=False, comment='主用接入端信息')
    main_devices = Column(String(100), nullable=False, comment='主用相关设备ip')
    backup_ip = Column(String(15), comment='备用登录ip')
    backup_vlan = Column(String(4), comment='备用网管vlan')
    backup_way = Column(VARCHAR(6), comment='备用方式')
    backup_topology = Column(ForeignKey('device_topology.topology', ondelete='SET NULL', onupdate='CASCADE'),
                             index=True, comment='备用拓扑')
    backup_access = Column(String(255), comment='备用接入端信息')
    backup_devices = Column(String(100), comment='备用相关设备')
    switch_way = Column(String(10), comment='切换方式')
    remark = Column(VARCHAR(500), comment='备注信息')
    monotony = Column(VARCHAR(30), unique=True, comment='调单号')
    circuit_code = Column(VARCHAR(30), unique=True, comment='电路编号')
    scenes = Column(String(5), nullable=False, comment='应用场景')
    is_protect = Column(String(2), nullable=False, comment='上联交换机/分组是否有保护')
    is_room = Column(String(2), nullable=False, comment='OLT与交换机/分组是否同机房')
    device_name = Column(String(30), nullable=False, comment='上联交换机/分组设备名称')
    longitude_latitude = Column(VARCHAR(20), comment='经纬度')
    open_time = Column(Date, comment='开通时间')


class NetworkAccount(Base):
    __tablename__ = 'network_account'

    __table_args__ = (
        Index('monotony_circuit_code', 'monotony', 'circuit_code', unique=True),
    )

    network_id = Column(INTEGER(6), Sequence('network_account_id_seq'), primary_key=True, comment='网络台账id')
    place = Column(VARCHAR(10), nullable=False, comment='所属区域')
    name = Column(VARCHAR(50), nullable=False, comment='客户名称')
    vlan = Column(VARCHAR(10), comment='客户vlan')
    ip_address = Column(VARCHAR(255), nullable=False, unique=True, comment='客户ip地址')
    mask_router_dns = Column(String(255), nullable=False, comment='掩码、网关、DNS')
    sub_interface = Column(VARCHAR(5), comment='子接口')
    topology = Column(ForeignKey('device_topology.topology', ondelete='SET NULL', onupdate='CASCADE'),
                      index=True, comment='交换机拓扑')
    access_information = Column(String(255), comment='接入端信息')
    relate_device = Column(String(255), nullable=False, comment='相关设备')
    bandwidth = Column(VARCHAR(6), comment='带宽')
    business_type = Column(VARCHAR(10), comment='业务类型')
    user_address = Column(VARCHAR(200), comment='客户地址')
    username = Column(VARCHAR(20), comment='联系人')
    user_phone = Column(VARCHAR(11), comment='联系人电话')
    user_manager = Column(VARCHAR(20), comment='客户经理')
    manager_phone = Column(VARCHAR(11), comment='客户经理电话')
    remark = Column(VARCHAR(500), comment='备注信息')
    finnish_time = Column(String(100), comment='竣工时间')
    product_code = Column(VARCHAR(30), unique=True, comment='产品号码')
    monotony = Column(VARCHAR(30), comment='调单号')
    circuit_code = Column(VARCHAR(30), comment='电路编号')
    is_open = Column(VARCHAR(2), comment='是否开放80端口')


class DeviceAccount(Base):
    __tablename__ = 'device_account'

    device_id = Column(INTEGER(6), Sequence('device_account_id_seq'), primary_key=True, comment='设备id')
    region = Column(String(15), nullable=False, comment='区域')
    place = Column(VARCHAR(8), nullable=False, comment='所属区域')
    device_name = Column(VARCHAR(25), nullable=False, unique=True, comment='设备名称')
    device_alias = Column(VARCHAR(30), nullable=False, unique=True, comment='设备别称')
    manage_ip = Column(VARCHAR(128), nullable=False, unique=True, comment='设备ip')
    network_level = Column(VARCHAR(15), comment='网络层次')
    manufacture = Column(VARCHAR(5), comment='厂商')
    device_type = Column(VARCHAR(15), comment='设备类型')
    device_model = Column(VARCHAR(20), comment='设备型号')
    room_name = Column(VARCHAR(50), comment='机房名称')
    remark = Column(VARCHAR(500), comment='备注信息')

    @staticmethod
    def on_update_(target, new_value, old_value, initiator):
        if str(old_value) != "symbol('NO_VALUE')" and new_value and old_value != new_value:
            DeviceAccount.change_topology_(new_value, old_value)

    @staticmethod
    def on_delete_(mapper, connection, target):
        device_alias = target.__dict__.get('device_alias')
        DeviceAccount.delete_topology_(device_alias)

    @staticmethod
    def change_topology_(new_value, old_value):
        results = session.query(DeviceTopology).filter(DeviceTopology.topology.like('%' + old_value + '%')).all()
        topology_list = [res.topology for res in results]
        new_topology_list = [str(topology).replace(old_value, new_value) for topology in topology_list]
        for index, topology in enumerate(new_topology_list):
            if topology != topology_list[index]:
                session.query(DeviceTopology).filter_by(topology=topology_list[index].replace("'", '"')).update(
                    {DeviceTopology.topology: topology.replace("'", '"')}, synchronize_session=False
                )

    @staticmethod
    def delete_topology_(device_alias):
        results = session.query(DeviceTopology).filter(DeviceTopology.topology.like('%' + device_alias + '%')).all()
        del_topology_list = [str(res.topology).replace("'", '"') for res in results]
        for del_topology in del_topology_list:
            session.query(DeviceTopology).filter(DeviceTopology.topology == del_topology).delete()


class DevicePort(Base):
    __tablename__ = 'device_port'

    __table_args__ = (
        Index('device_port', 'device_name', 'device_alias', 'manage_ip', 'port', unique=True),
    )

    port_id = Column(INTEGER(6), primary_key=True, comment='端口id')
    device_name = Column(ForeignKey('device_account.device_name', ondelete='CASCADE', onupdate='CASCADE'),
                         nullable=False, index=True, comment='所属设备')
    device_alias = Column(ForeignKey('device_account.device_alias', ondelete='CASCADE', onupdate='CASCADE'),
                          nullable=False, index=True, comment='所属设备名称')
    region = Column(ForeignKey('device_account.region', ondelete='CASCADE', onupdate='CASCADE'), nullable=False,
                    index=True, comment='所属区域')
    port_bandwidth = Column(String(5), nullable=False, comment='端口带宽')
    manage_ip = Column(ForeignKey('device_account.manage_ip', ondelete='CASCADE', onupdate='CASCADE'), nullable=False,
                       index=True, comment='所属管理ip')
    port = Column(VARCHAR(30), nullable=False, comment='设备端口')
    describe = Column(VARCHAR(100), comment='端口描述')

    @staticmethod
    def on_update_(target, new_port, old_port, initiator):
        if str(old_port) != "symbol('NO_VALUE')" and new_port and old_port != new_port:
            device_alias = target.__dict__.get('device_alias')
            old_device_port = device_alias + ':' + old_port
            new_device_port = device_alias + ':' + new_port
            DevicePort.change_topology_(new_device_port, old_device_port)

    @staticmethod
    def on_delete_(mapper, connection, target):
        device_alias = target.__dict__.get('device_alias')
        port = target.__dict__.get('port')
        device_port = device_alias + ':' + port
        DevicePort.delete_topology_(device_port)

    @staticmethod
    def delete_topology_(device_port):
        results = session.query(DeviceTopology).filter(DeviceTopology.topology.like('%' + device_port + '%')).all()
        topology_list = [eval(res.topology) for res in results]
        del_topology_list = [topology for topology in topology_list if device_port in topology]
        for del_topology in del_topology_list:
            session.query(DeviceTopology).filter(
                DeviceTopology.topology == str(del_topology).replace("'", '"')
            ).delete()

    @staticmethod
    def change_topology_(new_device_port, old_device_port):
        results = session.query(DeviceTopology).filter(DeviceTopology.topology.like('%' + old_device_port + '%')).all()
        topology_list = [eval(res.topology) for res in results]
        new_topology_list = [[new_device_port if res == old_device_port else res for res in topology] for
                             topology in topology_list]
        for index, topology in enumerate(new_topology_list):
            if str(topology) != str(topology_list[index]):
                session.query(DeviceTopology).filter_by(topology=str(topology_list[index]).replace("'", '"')).update(
                    {DeviceTopology.topology: str(topology).replace("'", '"')}, synchronize_session=False
                )


listen(DevicePort.port, 'set', DevicePort.on_update_)
listen(DeviceAccount.device_alias, 'set', DeviceAccount.on_update_)
listen(MultipleAccount.main_topology, 'set', DeviceAccount.on_update_)
listen(DevicePort, 'before_delete', DevicePort.on_delete_)
listen(DeviceAccount, 'before_delete', DeviceAccount.on_delete_)
