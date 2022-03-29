from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from apps.utils.util_tool import get_error_message
from apps.validates.network_validate import AddNetworkAccountForm

network_bp = Blueprint('network_data', __name__, url_prefix='/api/v1/network')


@network_bp.route('/search_account')
def search_network_account():
    pass


@network_bp.route('/add_account')
def add_network_account():
    print(request.form.get('mask_router_dns'))
    form = AddNetworkAccountForm(request.form)
    if form.validate():
        print(111)
    message = get_error_message(form.errors)
    return jsonify({'msg': message})


@network_bp.route('/modify_account')
def modify_network_account():
    pass


@network_bp.route('/delete_account')
def delete_network_account():
    pass
