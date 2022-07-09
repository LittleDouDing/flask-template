import asyncio
from apps.models import get_value
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from apps.database.port import PortManage
from apps.validates.port_validate import GetPortForm, DeletePortForm, AddPortForm, ModifyPortForm
from apps.utils.util_tool import get_error_message, get_form_data
from decorators import file_required
from apps.utils.route_tool import handle_route
from decorators import permission_required

port_bp = Blueprint('port_data', __name__, url_prefix='/api/v1/port')


@port_bp.route('/add_port', methods=['POST'])
@permission_required('configure')
@jwt_required()
def add_device_port():
    form = AddPortForm(request.form)
    if form.validate():
        port = PortManage(datadict=get_form_data(form), handle_type='add_port')
        result, code = handle_route(port, del_redis_key='port')
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@port_bp.route('/import_port', methods=['POST'])
@file_required()
@permission_required('configure')
@jwt_required()
def import_device_port():
    uploaded_file = request.files.get('file')
    port = PortManage(upload_file=uploaded_file, handle_type='import_device_port')
    result, code = handle_route(port, del_redis_key='port')
    return jsonify(result), code


@port_bp.route('/export_port', methods=['GET'])
@jwt_required()
def export_device_port():
    port = PortManage(handle_type='export_device_port')
    if port.data.get('result'):
        return port.data.get('data')
    return jsonify({'msg': port.data.get('message'), 'code': 403}), 403


@port_bp.route('/delete_port', methods=['POST'])
@permission_required('configure')
@jwt_required()
def delete_device_port():
    form = DeletePortForm(request.form)
    if form.validate():
        port = PortManage(datadict=get_form_data(form), handle_type='delete_port')
        result, code = handle_route(port, del_redis_key='port')
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@port_bp.route('/modify_port', methods=['POST'])
@permission_required('configure')
@jwt_required()
def modify_device_port():
    form = ModifyPortForm(request.form)
    if form.validate():
        port = PortManage(datadict=get_form_data(form), handle_type='modify_port')
        result, code = handle_route(port, del_redis_key='port')
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@port_bp.route('/search_port', methods=['GET'])
@jwt_required()
def search_device_port():
    form = GetPortForm(request.args)
    if form.validate():
        page = str(form.page.data) if form.page.data else '1'
        redis_key = 'page_' + page + '_' + str(get_form_data(form).items()) + '_device_ports'
        ports_data = asyncio.run(get_value(redis_key))
        if ports_data:
            return jsonify({'msg': 'success', 'data': eval(ports_data), 'code': 200}), 200
        port = PortManage(datadict=get_form_data(form), handle_type='get_port')
        result, code = handle_route(port, set_redis_key=redis_key)
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403
