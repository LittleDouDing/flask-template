# coding: utf-8
from sqlalchemy import JSON, String, Column, Sequence, ForeignKey, Index
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.event import listen
from sqlalchemy import events, event
from sqlalchemy.orm import relationship
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


class DeviceAccount(Base):
    __tablename__ = 'device_account'

    device_id = Column(INTEGER(6), Sequence('device_account_id_seq'), primary_key=True, comment='设备id')
    region = Column(String(15), nullable=False, comment='区域')
    place = Column(VARCHAR(10), nullable=False, comment='所属区域')
    device_name = Column(VARCHAR(25), nullable=False, unique=True, comment='设备名称')
    device_alias = Column(VARCHAR(30), nullable=False, unique=True, comment='设备别称')
    manage_ip = Column(VARCHAR(128), nullable=False, unique=True, comment='设备ip')
    network_level = Column(VARCHAR(15), comment='网络层次')
    manufacture = Column(VARCHAR(5), comment='厂商')
    device_type = Column(VARCHAR(15), comment='设备类型')
    device_model = Column(VARCHAR(20), comment='设备型号')
    room_name = Column(VARCHAR(50), comment='机房名称')
    remark = Column(VARCHAR(500), comment='备注信息')


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

    device_account = relationship('DeviceAccount', primaryjoin='DevicePort.device_alias == DeviceAccount.device_alias')
    device_account1 = relationship('DeviceAccount', primaryjoin='DevicePort.device_name == DeviceAccount.device_name')
    device_account2 = relationship('DeviceAccount', primaryjoin='DevicePort.manage_ip == DeviceAccount.manage_ip')
    device_account3 = relationship('DeviceAccount', primaryjoin='DevicePort.region == DeviceAccount.region')

    @staticmethod
    def on_update_(target, new_port, old_port, initiator):
        if str(old_port) != "symbol('NO_VALUE')" and new_port and old_port != new_port:
            device_alias = target.__dict__.get('device_alias')
            old_device_port = device_alias + ':' + old_port
            new_device_port = device_alias + ':' + new_port
            DevicePort.change_topology_(new_device_port, old_device_port)

    @staticmethod
    def on_delete_(mapper, connection, target):
        print(target)
        print(123)

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


class DeviceTopology(Base):
    __tablename__ = 'device_topology'

    topology_id = Column(INTEGER(6), Sequence('topology_id_seq'), primary_key=True, comment='设备拓扑id')
    topology = Column(String(500), nullable=False, unique=True, comment='交换机拓扑')


class MultipleAccount(Base):
    __tablename__ = 'multiple_account'

    __table_args__ = (
        Index('place_vlan', 'place', 'band_vlan', 'iptv_vlan', 'voice_vlan', unique=True),
    )

    multiple_id = Column(INTEGER(6), primary_key=True, comment='多元化id')
    multiple_name = Column(VARCHAR(50), nullable=False, unique=True, comment='多元化名称')
    place = Column(VARCHAR(8), nullable=False, comment='所属区域')
    band_vlan = Column(VARCHAR(4), comment='宽带vlan')
    iptv_vlan = Column(VARCHAR(4), comment='IPTV vlan')
    voice_vlan = Column(VARCHAR(4), comment='语音vlan')
    multiple_ip = Column(JSON, nullable=False, comment='主备用登录ip')
    manage_vlan = Column(JSON, nullable=False, comment='主备用网管vlan')
    use_way = Column(JSON, nullable=False, comment='主备用使用方式')
    topology = Column(JSON, nullable=False, comment='主备用拓扑')
    access_information = Column(String(250), nullable=False, comment='接入端信息')
    relate_devices = Column(JSON, nullable=False, comment='主备用相关设备ip')
    remark = Column(VARCHAR(250), comment='备注信息')
    monotony = Column(VARCHAR(30), comment='调单号')
    circuit_code = Column(VARCHAR(30), comment='电路编号')


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
    mask_router_dns = Column(JSON, nullable=False, comment='掩码、网关、DNS')
    sub_interface = Column(VARCHAR(5), comment='子接口')
    topology = Column(ForeignKey('device_topology.topology', ondelete='CASCADE', onupdate='CASCADE'),
                      nullable=False,
                      index=True, comment='交换机拓扑')
    access_information = Column(String(255), comment='接入端信息')
    relate_device = Column(JSON, nullable=False, comment='相关设备')
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

    device_topology = relationship('DeviceTopology')


# listen(DevicePort.port, 'set', DevicePort.on_update_)
listen(DevicePort, 'after_update', DevicePort.on_delete_)
