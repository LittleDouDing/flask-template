from flask import request
import asyncio
from apps.models import set_value, get_value


def handle_before_request():
    ip_address = request.remote_addr
    path = request.path
    if path not in ['/api/v1/user/login', '/api/v1/admin/login', '/api/v1/get_code']:
        user = asyncio.run(get_value(ip_address))
        if not user:
            return {'msg': 'Please Login again to perform this operation', 'code': 403}, 403
        asyncio.run(set_value(ip_address, user, expire=1800))
