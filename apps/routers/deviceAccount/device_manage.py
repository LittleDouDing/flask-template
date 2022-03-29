import asyncio

from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from apps.models.device import DeviceManage
from apps.models.general import UserManager
from apps.models import get_value, set_value
from apps.validates.device_validate import AddDeviceAccountFrom, DeleteDeviceAccountForm, ModifyDeviceAccountForm, \
    SearchDeviceAccountForm
from apps.utils.util_tool import get_error_message

device_bp = Blueprint('device_data', __name__, url_prefix='/api/v1/device')


@device_bp.route('/add_account', methods=['POST'])
@jwt_required()
def add_device_account():
    user = UserManager(datadict={'username': get_jwt_identity()}, handle_type='get_author')
    if user.author == 'check':
        return jsonify({'msg': 'The current user does not have permission to add an account', 'code': 403}), 403
    form = AddDeviceAccountFrom(request.form)
    if form.validate():
        device = DeviceManage(request.form, handle_type='add_device_account')
        message = device.data.get('message')
        if device.data.get('result'):
            return jsonify({'msg': message, 'code': 200}), 200
        return jsonify({'msg': message, 'code': 403}), 403
    message = get_error_message(form.errors)
    return jsonify({'msg': message, 'code': 403}), 403


@device_bp.route('/modify_account', methods=['POST'])
@jwt_required()
def modify_device_account():
    user = UserManager(datadict={'username': get_jwt_identity()}, handle_type='get_author')
    if user.author == 'check':
        return jsonify({'msg': 'The current user does not have permission to add an account', 'code': 403}), 403
    form = ModifyDeviceAccountForm(request.form)
    if form.validate():
        device = DeviceManage(request.form, handle_type='modify_device_account')
        message = device.data.get('message')
        if device.data.get('result'):
            return jsonify({'msg': message, 'code': 200}), 200
        return jsonify({'msg': message, 'code': 403}), 403
    message = get_error_message(form.errors)
    return jsonify({'msg': message, 'code': 403}), 403


@device_bp.route('/delete_account', methods=['POST'])
@jwt_required()
def delete_device_account():
    user = UserManager(datadict={'username': get_jwt_identity()}, handle_type='get_author')
    if user.author == 'check':
        return jsonify({'msg': 'The current user does not have permission to add an account', 'code': 403}), 403
    form = DeleteDeviceAccountForm(request.form)
    if form.validate():
        device = DeviceManage(request.form, handle_type='delete_device_account')
        message = device.data.get('message')
        if device.data.get('result'):
            return jsonify({'msg': message, 'code': 200}), 200
        return jsonify({'msg': message, 'code': 403}), 403
    message = get_error_message(form.errors)
    return jsonify({'msg': message, 'code': 403}), 403


@device_bp.route('/search_account', methods=['GET'])
@jwt_required()
def search_device_account():
    form = SearchDeviceAccountForm(request.args)
    if form.validate():
        page = str(form.page.data) if form.page.data else '1'
        accounts_data = asyncio.run(get_value('page_' + page + '_' + str(request.args) + '_device_accounts'))
        if accounts_data:
            return jsonify({'msg': 'success', 'data': eval(accounts_data), 'code': 200}), 200
        device = DeviceManage(request.args, handle_type='search_device_account')
        message = device.data.get('message')
        if device.data.get('result'):
            data = device.data.get('data')
            asyncio.run(set_value('page_' + page + '_' + str(request.args) + '_device_accounts', str(data)))
            return jsonify({'msg': message, 'data': data, 'code': 200}), 200
        return jsonify({'msg': message, 'code': 403}), 403
    message = get_error_message(form.errors)
    return jsonify({'msg': message, 'code': 403}), 403
