import re
import asyncio
from apps.models import db
from wtforms import ValidationError
from apps.validates import Config
from apps.models import set_value


def get_topology(result):
    topology = ''
    for index, item in enumerate(result):
        device, port = item.split(':')
        if index % 2 == 0:
            if device in topology:
                topology += '(' + port + ')'
            else:
                topology += device + '(' + port + ')'
        else:
            topology += '<----->' + '(' + port + ')' + device
    return topology


def get_network_topology(topology, access_list):
    topology = topology + '(' + access_list[0].split(':')[1] + ')' + '<----->'
    for item in access_list[1:-1]:
        topology += item + '<----->'
    topology += access_list[-1]
    return topology


def check_topology(device_list):
    device_alias_list = [(device_alias.split(':')[0], device_alias.split(':')[1]) for device_alias in device_list]
    for device_alia, port in device_alias_list:
        result = get_device_account(device_alia, port)
        if not result:
            return {'message': 'The ' + device_alia + ':' + port + ' does not exist in port table', 'result': False}
    return {'result': True}


def get_device_account(device_alias, port):
    from apps.database.port import DevicePort
    session = db.session
    result = session.query(DevicePort).filter_by(device_alias=device_alias, port=port).first()
    return result


def get_device_ip(device_list):
    device_name_ips = []
    for device in device_list:
        device_alias, port = device.split(':')[0], device.split(':')[1]
        result = get_device_account(device_alias, port)
        if result:
            device_name_ip = result.device_alias + '：' + result.manage_ip
            device_name_ips.append(device_name_ip)
    return list(set(device_name_ips))


def handle_route(obj, set_redis_key=None, del_redis_key=None):
    from apps.utils.util_tool import delete_relate_keys
    message = obj.data.get('message')
    if obj.data.get('result'):
        asyncio.run(set_value(set_redis_key, str(obj.data.get('data')))) if set_redis_key else None
        delete_relate_keys(del_redis_key) if del_redis_key else None
        if obj.data.get('data'):
            return {'msg': obj.data.get('message'), 'data': obj.data.get('data'), 'code': 200}, 200
        return {'msg': message, 'code': 200}, 200
    return {'msg': message, 'code': 403}, 403


def handle_filed(filed, filed_name, data, regex, is_topology=False):
    if not isinstance(filed.data, dict):
        raise ValidationError('The data format of the ' + filed_name + ' is not an dict')
    for item in data.items():
        if is_topology:
            # 如果是topology
            if not isinstance(item[1], list):
                raise ValidationError('The data format of the ' + item[1] + ' is not a list')
            for x in item[1]:
                if not re.match(regex, x):
                    raise ValidationError('The device port ' + x + ' does not conform to the specification')
        else:
            keys = Config.keys()
            if not re.match(keys, item[0]) or not isinstance(item[1], str) or not re.match(regex, item[1]):
                raise ValidationError('The data format of the ' + str(item) + ' is not a legal data')
