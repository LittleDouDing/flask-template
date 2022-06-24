import asyncio
from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required
from apps.database.device import DeviceManage
from apps.models import get_value
from apps.validates.device_validate import AddDeviceAccountForm, DeleteDeviceAccountForm, ModifyDeviceAccountForm, \
    SearchDeviceAccountForm
from apps.utils.util_tool import get_error_message, get_form_data
from apps.utils.route_tool import handle_route
from decorators import permission_required, file_required

device_bp = Blueprint('device_data', __name__, url_prefix='/api/v1/device')


@device_bp.route('/import_account', methods=['POST'])
@file_required()
@permission_required('configure')
@jwt_required()
def import_device_account():
    uploaded_file = request.files.get('file')
    device = DeviceManage(upload_file=uploaded_file, handle_type='import_device_account')
    result, code = handle_route(device, del_redis_key='device')
    return jsonify(result), code


@device_bp.route('/add_account', methods=['POST'])
@permission_required('configure')
@jwt_required()
def add_device_account():
    form = AddDeviceAccountForm(request.form)
    if form.validate():
        device = DeviceManage(datadict=get_form_data(form), handle_type='add_device_account')
        result, code = handle_route(device, del_redis_key='device')
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@device_bp.route('/modify_account', methods=['POST'])
@permission_required('configure')
@jwt_required()
def modify_device_account():
    form = ModifyDeviceAccountForm(request.form)
    if form.validate():
        device = DeviceManage(datadict=get_form_data(form), handle_type='modify_device_account')
        result, code = handle_route(device, del_redis_key='device')
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@device_bp.route('/delete_account', methods=['POST'])
@permission_required('configure')
@jwt_required()
def delete_device_account():
    form = DeleteDeviceAccountForm(request.form)
    if form.validate():
        device = DeviceManage(datadict=get_form_data(form), handle_type='delete_device_account')
        result, code = handle_route(device, del_redis_key='device')
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@device_bp.route('/search_account', methods=['GET'])
@jwt_required()
def search_device_account():
    form = SearchDeviceAccountForm(request.args)
    if form.validate():
        page = str(form.page.data) if form.page.data else '1'
        redis_key = 'page_' + page + '_' + str(get_form_data(form).items()) + '_device_accounts'
        accounts_data = asyncio.run(get_value(redis_key))
        if accounts_data:
            return jsonify({'msg': 'success', 'data': eval(accounts_data), 'code': 200}), 200
        device = DeviceManage(datadict=get_form_data(form), handle_type='search_device_account')
        result, code = handle_route(device, set_redis_key=redis_key)
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@device_bp.route('/export_account', methods=['GET'])
@jwt_required()
def export_device_account():
    device = DeviceManage(handle_type='export_device_account')
    if device.data.get('result'):
        return device.data.get('data')
    return jsonify({'msg': device.data.get('message'), 'code': 403}), 403
