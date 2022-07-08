from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from apps.utils.util_tool import get_error_message, get_form_data
from apps.utils.route_tool import handle_route
from decorators import permission_required
from apps.database.network import NetworkManage
from werkzeug.datastructures import ImmutableMultiDict
from decorators import file_required
from apps.models import get_value
import asyncio
from apps.validates.network_validate import AddNetworkAccountForm, DeleteNetworkAccountForm, ModifyNetworkAccountForm, \
    GetNetworkAccountForm

network_bp = Blueprint('network_data', __name__, url_prefix='/api/v1/network')


@network_bp.route('/search_account', methods=['GET'])
@jwt_required()
def search_topology():
    form = GetNetworkAccountForm(request.args)
    if form.validate():
        page = str(form.page.data) if form.page.data else '1'
        redis_key = 'page_' + page + '_' + str(get_form_data(form).items()).replace(':', '') + '_network_account'
        accounts_data = asyncio.run(get_value(redis_key))
        if accounts_data:
            return jsonify({'msg': 'success', 'data': eval(accounts_data), 'code': 200}), 200
        topology = NetworkManage(datadict=get_form_data(form), handle_type='search_network_account')
        result, code = handle_route(topology, set_redis_key=redis_key)
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@network_bp.route('/add_account', methods=['POST'])
@permission_required('configure')
@jwt_required()
def add_network_account():
    json_data = request.json.items() if request.json else ''
    network_data = [(item[0], item[1]) for item in json_data]
    form = AddNetworkAccountForm(ImmutableMultiDict(network_data))
    if form.validate():
        network = NetworkManage(datadict=get_form_data(form), handle_type='add_network_account')
        result, code = handle_route(network, del_redis_key='network')
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@network_bp.route('/modify_account', methods=['POST'])
@permission_required('configure')
@jwt_required()
def modify_topology():
    json_data = request.json.items() if request.json else ''
    multiple_data = [(item[0], item[1]) for item in json_data]
    form = ModifyNetworkAccountForm(ImmutableMultiDict(multiple_data))
    if form.validate():
        topology = NetworkManage(datadict=get_form_data(form), handle_type='modify_network_account')
        result, code = handle_route(topology, del_redis_key='network')
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@network_bp.route('/delete_account', methods=['POST'])
@permission_required('configure')
@jwt_required()
def delete_topology():
    form = DeleteNetworkAccountForm(request.form)
    if form.validate():
        topology = NetworkManage(datadict=get_form_data(form), handle_type='delete_network_account')
        result, code = handle_route(topology, del_redis_key='network')
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@network_bp.route('/export_account', methods=['GET'])
@jwt_required()
def export_topology():
    multiple = NetworkManage(handle_type='export_network_account')
    if multiple.data.get('result'):
        return multiple.data.get('data')
    return jsonify({'msg': multiple.data.get('message'), 'code': 403}), 403


@network_bp.route('/import_account', methods=['POST'])
@file_required()
@permission_required('configure')
@jwt_required()
def import_device_port():
    uploaded_file = request.files.get('file')
    multiple = NetworkManage(upload_file=uploaded_file, handle_type='import_network_account')
    result, code = handle_route(multiple, del_redis_key='network')
    return jsonify(result), code
