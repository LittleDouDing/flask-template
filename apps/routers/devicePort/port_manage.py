import asyncio
from apps.models import get_value, set_value
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from apps.models.port import PortManage
from apps.models.general import UserManager
from apps.validates.port_validate import GetPortForm, DeletePortForm
from apps.utils.util_tool import get_error_message

port_bp = Blueprint('port_data', __name__, url_prefix='/api/v1/port')


@port_bp.route('/add_port', methods=['POST'])
@jwt_required()
def add_port():
    user = UserManager(datadict={'username': get_jwt_identity()}, handle_type='get_author')
    if user.author == 'check':
        return jsonify({'msg': 'The current user does not have permission to add an account', 'code': 403}), 403
    file = request.files.get('file')
    if not file or file.filename.rsplit('.')[1] not in ['xls', 'xlsx']:
        return {'msg': 'The file does not exist or the file format is not xls or xlsx', 'code': 403}, 403
    res = PortManage(datadict=file.read(), handle_type='add_port')
    return jsonify({'msg': res.data.get('message'), 'code': 200}), 200


@port_bp.route('/delete_port', methods=['POST'])
@jwt_required()
def delete_port():
    user = UserManager(datadict={'username': get_jwt_identity()}, handle_type='get_author')
    if user.author == 'check':
        return jsonify({'msg': 'The current user does not have permission to add an account', 'code': 403}), 403
    form = DeletePortForm(request.form)
    if form.validate():
        port = PortManage(datadict=request.form, handle_type='delete_port')
        message = port.data.get('message')
        if port.data.get('result'):
            return jsonify({'msg': message, 'code': 200}), 200
        return jsonify({'msg': message, 'code': 403}), 403
    message = get_error_message(form.errors)
    return jsonify({'msg': message, 'code': 403}), 403


@port_bp.route('/search_port', methods=['GET'])
@jwt_required()
def search_port():
    form = GetPortForm(request.args)
    if form.validate():
        form_data = {key: form.data[key] for key in form.data if form.data[key]}
        page = str(form.page.data) if form.page.data else '1'
        ports_data = asyncio.run(get_value('page_' + page + '_' + str(form_data.items()) + '_device_ports'))
        if ports_data:
            return jsonify({'msg': 'success', 'data': eval(ports_data), 'code': 200}), 200
        port = PortManage(datadict=form_data, handle_type='get_port')
        message = port.data.get('message')
        if port.data.get('result'):
            data = port.data.get('data')
            asyncio.run(set_value('page_' + page + '_' + str(form_data.items()) + '_device_ports', str(data)))
            return jsonify({'msg': message, 'data': data, 'code': 200}), 200
        return jsonify({'msg': message, 'code': 403}), 403
    message = get_error_message(form.errors)
    return jsonify({'msg': message, 'code': 403}), 403
