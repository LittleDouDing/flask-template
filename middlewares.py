from flask import request
from apps.utils.util_tool import check_illegal_data
import asyncio
from apps.models import set_value, get_value
from flask import make_response


def handle_before_request():
    ip_address = request.remote_addr
    path = request.path
    if path not in ['/api/v1/user/login', '/api/v1/admin/login', '/api/v1/get_code']:
        user = asyncio.run(get_value(ip_address))
        if not user:
            return {'msg': 'Please Login again to perform this operation', 'code': 403}
        asyncio.run(set_value(ip_address, user, expire=1800))


def handle_illegal_request():
    data_dict = request.form | request.args
    if check_illegal_data(str(data_dict.values())):
        return {'msg': 'The request parameter contains illegal characters', 'code': 405}


def handle_unauthorized(jwt_header):
    return make_response({'msg': 'The necessary token is missing', 'code': 422})


def handle_expired_token(jwt_header):
    return make_response({'msg': 'The necessary token is expired', 'code': 401})
