# coding: utf-8
from sqlalchemy import Date, JSON, String, Column, Sequence, Integer, ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# from urllib import parse
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# USERNAME = 'root'
# PASSWORD = parse.quote_plus('Lin123456@')

Base = declarative_base()
metadata = Base.metadata


class Admin(Base):
    __tablename__ = 'admin'

    username = Column(VARCHAR(20), primary_key=True, comment='管理员账号(OA账号)')
    password = Column(VARCHAR(255), nullable=False, comment='管理员密码')
    name = Column(VARCHAR(30), nullable=False, comment='管理员姓名')
    sex = Column(VARCHAR(2), nullable=False, comment='管理员性别')
    email = Column(VARCHAR(50), nullable=False, unique=True, comment='管理员邮箱')
    phone = Column(VARCHAR(11), nullable=False, unique=True, comment='管理员联系方式')


class DevicePort(Base):
    __tablename__ = 'device_port'

    port_id = Column(INTEGER(6), primary_key=True, comment='端口id')
    full_name = Column(ForeignKey('device_account.full_name', ondelete='CASCADE', onupdate='CASCADE'), nullable=False,
                       unique=True, comment='设备全称')
    device_name = Column(ForeignKey('device_account.device_name', ondelete='CASCADE', onupdate='CASCADE'),
                         nullable=False, unique=True, comment='设备名称')
    device_type = Column(ForeignKey('device_account.device_type', ondelete='CASCADE', onupdate='CASCADE'),
                         nullable=False, index=True, comment='设备类型')
    ports = Column(JSON, nullable=False, comment='相关设备端口')

    device_account = relationship('DeviceAccount', primaryjoin='DevicePort.device_name == DeviceAccount.device_name')
    device_account1 = relationship('DeviceAccount', primaryjoin='DevicePort.device_type == DeviceAccount.device_type')
    device_account2 = relationship('DeviceAccount', primaryjoin='DevicePort.full_name == DeviceAccount.full_name')


class DeviceTopology(Base):
    __tablename__ = 'device_topology'

    topology_id = Column(Integer, primary_key=True, comment='设备拓扑id')
    topology = Column(JSON, comment='拓扑信息')


class DeviceAccount(Base):
    __tablename__ = 'device_account'

    device_id = Column(INTEGER(6), Sequence('device_account_id_seq'), primary_key=True, comment='设备id')
    full_name = Column(VARCHAR(25), nullable=False, unique=True, comment='设备全称')
    device_type = Column(VARCHAR(10), nullable=False, index=True, comment='Bras')
    place = Column(VARCHAR(10), nullable=False, comment='所属区域')
    device_name = Column(VARCHAR(30), nullable=False, unique=True, comment='设备名称')
    manage_ip = Column(VARCHAR(128), nullable=False, unique=True, comment='设备ip')
    room_name = Column(VARCHAR(50), nullable=False, comment='机房名称')
    manufacture = Column(VARCHAR(5), nullable=False, comment='厂商')
    remark = Column(VARCHAR(500), comment='备注信息')
    register_port = Column(VARCHAR(20), comment='注册接口')
    band_port = Column(VARCHAR(20), comment='宽带接口')
    iptv_port = Column(VARCHAR(20), comment='IPTV接口')
    loop_port = Column(VARCHAR(255), comment='交换机成环端口')


class MultipleAccount(Base):
    __tablename__ = 'multiple_account'

    multiple_name = Column(String(255), primary_key=True, comment='多元化名称')
    multiple_ip = Column(JSON, nullable=False, comment='主备用登录ip')
    band_vlan = Column(String(255), comment='宽带vlan')
    iptv_vlan = Column(String(255), comment='IPTV vlan')
    voice_vlan = Column(String(255), comment='语音vlan')
    manage_vlan = Column(JSON, nullable=False, comment='主备用网管vlan')
    use_way = Column(JSON, nullable=False, comment='主备用使用方式')
    topology = Column(JSON, nullable=False, comment='主备用拓扑')
    device_ip = Column(JSON, nullable=False, comment='主备用相关设备ip')
    remark = Column(String(500), comment='备注信息')
    monotony = Column(String(255), comment='调单号')
    circuit_code = Column(String(255), comment='电路编号')


class NetworkAccount(Base):
    __tablename__ = 'network_account'

    network_id = Column(INTEGER(6), Sequence('network_account_id_seq'), primary_key=True, comment='网络台账id')
    place = Column(VARCHAR(10), nullable=False, comment='所属区域')
    name = Column(VARCHAR(50), nullable=False, comment='客户名称')
    vlan = Column(VARCHAR(10), comment='客户vlan')
    ip_address = Column(VARCHAR(128), nullable=False, unique=True, comment='客户ip地址')
    mask_router_dns = Column(VARCHAR(255), nullable=False, comment='掩码、网关、DNS')
    sub_interface = Column(VARCHAR(5), comment='子接口')
    topology = Column(VARCHAR(300), nullable=False, comment='网络拓扑')
    access_information = Column(VARCHAR(200), comment='接入端信息')
    bandwidth = Column(VARCHAR(6), comment='带宽')
    user_address = Column(VARCHAR(200), comment='客户地址')
    username = Column(VARCHAR(20), comment='联系人')
    user_phone = Column(VARCHAR(11), comment='联系人电话')
    user_manager = Column(VARCHAR(20), comment='客户经理')
    manager_phone = Column(VARCHAR(11), comment='客户经理电话')
    remark = Column(VARCHAR(500), comment='备注信息')
    finnish_time = Column(Date, comment='竣工时间')
    product_code = Column(VARCHAR(30), unique=True, comment='产品号码')
    monotony = Column(VARCHAR(30), unique=True, comment='调单号')
    circuit_code = Column(VARCHAR(30), unique=True, comment='电路编号')
    is_open = Column(VARCHAR(2), comment='是否开放80端口')


class User(Base):
    __tablename__ = 'user'

    username = Column(VARCHAR(20), primary_key=True, comment='用户账号(OA账号)')
    password = Column(VARCHAR(255), nullable=False, comment='用户密码')
    author = Column(VARCHAR(10), nullable=False, comment='用户权限(查看、配置)')
    name = Column(VARCHAR(30), nullable=False, comment='用户姓名')
    sex = Column(VARCHAR(2), nullable=False, comment='用户性别')
    email = Column(VARCHAR(50), nullable=False, unique=True, comment='用户邮箱')
    phone = Column(VARCHAR(11), nullable=False, unique=True, comment='用户联系方式')

# def conn_database():
#     # 初始化数据库连接:
#     engine = create_engine(f'mysql+pymysql://{USERNAME}:{PASSWORD}@127.0.0.1:3306/ledgersystem?charset=utf8')
#     # 创建DBSession类型:
#     session = sessionmaker(bind=engine)
#     return session()
