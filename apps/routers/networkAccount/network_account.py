from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from apps.utils.util_tool import get_error_message, get_user_author, get_form_data, handle_route
from apps.models.network import NetworkManage
from werkzeug.datastructures import ImmutableMultiDict
from apps.validates.network_validate import AddNetworkAccountForm

network_bp = Blueprint('network_data', __name__, url_prefix='/api/v1/network')


@network_bp.route('/search_account')
@jwt_required()
def search_network_account():
    pass


@network_bp.route('/search_device_topology')
@jwt_required()
def search_device_topology():
    pass


@network_bp.route('/add_account', methods=['POST'])
@jwt_required()
def add_network_account():
    if get_user_author() == 'check':
        return jsonify({'msg': 'The current user does not have permission to add an account', 'code': 403}), 403
    json_data = request.json.items() if request.json else ''
    network_data = [(item[0], item[1]) for item in json_data]
    form = AddNetworkAccountForm(ImmutableMultiDict(network_data))
    # form = AddNetworkAccountForm(request.form)
    if form.validate():
        return jsonify({'111': 111})
        # network = NetworkManage(datadict=get_form_data(form), handle_type='add_network_account')
        # result, code = handle_route(network, del_redis_key='network')
        # return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@network_bp.route('/modify_account')
@jwt_required()
def modify_network_account():
    pass


@network_bp.route('/delete_account')
@jwt_required()
def delete_network_account():
    pass
