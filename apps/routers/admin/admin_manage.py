from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from apps.validates.admin_validate import AddUserForm, GetAllUserForm, DeleteUserForm, ChangeUserPasswordForm, \
    ChangeUserInfoForm
from apps.database.admin import AdminManager
from apps.utils.util_tool import get_error_message, get_form_data
from apps.utils.route_tool import handle_route
from decorators import admin_required
from apps.models import get_value
import asyncio

admin_bp = Blueprint('admin_data', __name__, url_prefix='/api/v1/admin')


@admin_bp.route('/add_user', methods=["POST"])
@admin_required()
@jwt_required()
def admin_add_user():
    form = AddUserForm(request.form)
    if form.validate():
        user = AdminManager(get_form_data(form), handle_type='add_user')
        result, code = handle_route(user, del_redis_key='user')
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@admin_bp.route('/delete_user', methods=["POST"])
@admin_required()
@jwt_required()
def admin_delete_user():
    form = DeleteUserForm(request.form)
    if form.validate():
        user = AdminManager(get_form_data(form), handle_type='delete_user')
        result, code = handle_route(user, del_redis_key='user')
        return jsonify(result), code
    return {'msg': get_error_message(form.errors), 'code': 403}, 403


@admin_bp.route('/change_user_password', methods=["POST"])
@admin_required()
@jwt_required()
def admin_change_user_password():
    form = ChangeUserPasswordForm(request.form)
    if form.validate():
        user = AdminManager(get_form_data(form), handle_type='change_user_password')
        result, code = handle_route(user, del_redis_key='user')
        return jsonify(result), code
    return {'msg': get_error_message(form.errors), 'code': 403}, 403


@admin_bp.route('/modify_user_info', methods=["POST"])
@admin_required()
@jwt_required()
def admin_modify_user_info():
    form = ChangeUserInfoForm(request.form)
    if form.validate():
        user = AdminManager(get_form_data(form), handle_type='modify_user_info')
        result, code = handle_route(user, del_redis_key='user')
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@admin_bp.route('/all_users', methods=["GET"])
@admin_required()
@jwt_required()
def get_all_users():
    form = GetAllUserForm(request.args)
    if form.validate():
        page = str(form.page.data) if form.page.data else '1'
        redis_key = 'page_' + page + '_' + str(get_form_data(form).items()) + '_users'
        users_info = asyncio.run(get_value(redis_key))
        if users_info:
            return jsonify({'msg': 'success', 'data': eval(users_info), 'code': 200}), 200
        users = AdminManager(get_form_data(form), handle_type='get_all_users')
        result, code = handle_route(users, set_redis_key=redis_key)
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403
