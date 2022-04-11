import asyncio
from apps.models import get_value
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from apps.models.port import PortManage
from apps.models.general import UserManager
from apps.validates.port_validate import GetPortForm, DeletePortForm
from apps.utils.util_tool import get_error_message, handle_route, get_form_data, get_user_author

port_bp = Blueprint('port_data', __name__, url_prefix='/api/v1/port')


@port_bp.route('/add_port', methods=['POST'])
@jwt_required()
def add_port():
    if get_user_author() == 'check':
        return jsonify({'msg': 'The current user does not have permission to add an account', 'code': 403}), 403
    file = request.files.get('file')
    if not file or file.filename.rsplit('.')[1] not in ['xls', 'xlsx']:
        return {'msg': 'The file does not exist or the file format is not xls or xlsx', 'code': 403}, 403
    res = PortManage(datadict={'file': file.read()}, handle_type='add_port')
    return jsonify({'msg': res.data.get('message'), 'code': 200}), 200


@port_bp.route('/delete_port', methods=['POST'])
@jwt_required()
def delete_port():
    if get_user_author() == 'check':
        return jsonify({'msg': 'The current user does not have permission to add an account', 'code': 403}), 403
    form = DeletePortForm(request.form)
    if form.validate():
        port = PortManage(get_form_data(form), handle_type='delete_port')
        result, code = handle_route(port, del_redis_key='port')
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@port_bp.route('/search_port', methods=['GET'])
@jwt_required()
def search_port():
    form = GetPortForm(request.args)
    if form.validate():
        page = str(form.page.data) if form.page.data else '1'
        redis_key = 'page_' + page + '_' + str(get_form_data(form).items()) + '_device_ports'
        ports_data = asyncio.run(get_value(redis_key))
        if ports_data:
            return jsonify({'msg': 'success', 'data': eval(ports_data), 'code': 200}), 200
        port = PortManage(get_form_data(form), handle_type='get_port')
        result, code = handle_route(port, set_redis_key=redis_key)
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403
