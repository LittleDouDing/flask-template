from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from apps.utils.util_tool import get_error_message, get_user_author, get_form_data, handle_route
from apps.models.network import NetworkManage
from werkzeug.datastructures import ImmutableMultiDict
from apps.validates.multiple_validate import AddMultipleAccountForm

multiple_bp = Blueprint('multiple_data', __name__, url_prefix='/api/v1/multiple')


@multiple_bp.route('/search_account')
@jwt_required()
def search_multiple_account():
    pass


@multiple_bp.route('/add_account', methods=['POST'])
@jwt_required()
def add_multiple_account():
    if get_user_author() == 'check':
        return jsonify({'msg': 'The current user does not have permission to add an account', 'code': 403}), 403
    json_data = request.json.items() if request.json else ''
    multiple_data = [(item[0], item[1]) for item in json_data]
    form = AddMultipleAccountForm(ImmutableMultiDict(multiple_data))
    if form.validate():
        return jsonify({'111': 111})
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@multiple_bp.route('/modify_account', methods=['POST'])
@jwt_required()
def modify_multiple_account():
    pass


@multiple_bp.route('/delete_account')
@jwt_required()
def delete_multiple_account():
    pass
