import asyncio
from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from apps.models.device import DeviceManage
from apps.models.general import UserManager
from apps.models import get_value
from apps.validates.device_validate import AddSwitchAccountForm, AddBrasAccountFrom, DeleteDeviceAccountForm, \
    ModifyBrasAccountForm, ModifySwitchAccountForm, SearchDeviceAccountForm
from apps.utils.util_tool import get_error_message, handle_route, get_form_data

device_bp = Blueprint('device_data', __name__, url_prefix='/api/v1/device')


@device_bp.route('/add_account', methods=['POST'])
@jwt_required()
def add_device_account():
    user = UserManager(datadict={'username': get_jwt_identity()}, handle_type='get_author')
    if user.author == 'check':
        return jsonify({'msg': 'The current user does not have permission to add an account', 'code': 403}), 403
    if request.form.get('device_type') == 'Bras':
        form = AddBrasAccountFrom(request.form)
    else:
        form = AddSwitchAccountForm(request.form)
    if form.validate():
        device = DeviceManage(get_form_data(form), handle_type='add_device_account')
        result, code = handle_route(device, del_redis_key='device')
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@device_bp.route('/modify_account', methods=['POST'])
@jwt_required()
def modify_device_account():
    user = UserManager(datadict={'username': get_jwt_identity()}, handle_type='get_author')
    if user.author == 'check':
        return jsonify({'msg': 'The current user does not have permission to add an account', 'code': 403}), 403
    if request.form.get('device_type') == 'Bras':
        form = ModifyBrasAccountForm(request.form)
    else:
        form = ModifySwitchAccountForm(request.form)
    if form.validate():
        device = DeviceManage(get_form_data(form), handle_type='modify_device_account')
        result, code = handle_route(device, del_redis_key='device')
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@device_bp.route('/delete_account', methods=['POST'])
@jwt_required()
def delete_device_account():
    user = UserManager(datadict={'username': get_jwt_identity()}, handle_type='get_author')
    if user.author == 'check':
        return jsonify({'msg': 'The current user does not have permission to add an account', 'code': 403}), 403
    form = DeleteDeviceAccountForm(request.form)
    if form.validate():
        device = DeviceManage(get_form_data(form), handle_type='delete_device_account')
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
        device = DeviceManage(get_form_data(form), handle_type='search_device_account')
        result, code = handle_route(device, set_redis_key=redis_key)
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403
