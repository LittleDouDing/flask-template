import asyncio
from apps.models import get_value, set_value
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from apps.models.topology import TopologyManage
from apps.models.general import UserManager
from werkzeug.datastructures import ImmutableMultiDict
from apps.validates.topology_validate import GetDevicePortForm, AddTopologyForm
from apps.utils.util_tool import get_error_message, handle_route

topology_bp = Blueprint('topology_data', __name__, url_prefix='/api/v1/topology')


@topology_bp.route('/add_topology', methods=['POST'])
@jwt_required()
def add_topology():
    form = AddTopologyForm(ImmutableMultiDict([('topology', request.json.get('topology'))]))
    if form.validate():
        topology = TopologyManage(datadict=request.json, handle_type='add_topology')
        message = topology.data.get('message')
        if topology.data.get('result'):
            return jsonify({'msg': message, 'code': 200}), 200
        return {'msg': message, 'code': 403}, 403
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@topology_bp.route('/delete_topology', methods=['POST'])
@jwt_required()
def delete_topology():
    pass


@topology_bp.route('/modify_topology', methods=['POST'])
@jwt_required()
def modify_topology():
    pass


@topology_bp.route('/search_topology', methods=['GET'])
@jwt_required()
def search_topology():
    pass


@topology_bp.route('/search_port', methods=['GET'])
@jwt_required()
def search_device_port():
    form = GetDevicePortForm(request.args)
    if form.validate():
        device_port = TopologyManage(datadict=request.args, handle_type='search_device_port')
        result, code = handle_route(device_port)
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403
