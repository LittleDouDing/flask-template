from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from apps.validates.admin_validate import AddUserForm, GetAllUserForm, DeleteUserForm, ChangeUserPasswordForm, \
    ChangeUserInfoForm
from apps.models.admin import AdminManager
from apps.utils.util_tool import get_error_message, handle_route
from apps.models import get_value
import asyncio

admin_bp = Blueprint('admin_data', __name__, url_prefix='/api/v1/admin')


@admin_bp.route('/add_user', methods=["POST"])
@jwt_required()
def admin_add_user():
    admin = AdminManager({'username': get_jwt_identity()}, handle_type='check_admin')
    if not admin.data.get('result'):
        return {'msg': admin.data.get('message'), 'code': 403}, 403
    form = AddUserForm(request.form)
    if form.validate():
        form_data = {key: form.data[key] for key in form.data if form.data[key]}
        user = AdminManager(form_data, handle_type='add_user')
        result, code = handle_route(user, del_redis_key='user')
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@admin_bp.route('/delete_user', methods=["POST"])
@jwt_required()
def admin_delete_user():
    admin = AdminManager({'username': get_jwt_identity()}, handle_type='check_admin')
    if not admin.data.get('result'):
        return {'msg': admin.data.get('message'), 'code': 403}, 403
    form = DeleteUserForm(request.form)
    if form.validate():
        form_data = {key: form.data[key] for key in form.data if form.data[key]}
        user = AdminManager(form_data, handle_type='delete_user')
        result, code = handle_route(user, del_redis_key='user')
        return jsonify(result), code
    return {'msg': get_error_message(form.errors), 'code': 403}, 403


@admin_bp.route('/change_user_password', methods=["POST"])
@jwt_required()
def admin_change_user_password():
    admin = AdminManager({'username': get_jwt_identity()}, handle_type='check_admin')
    if not admin.data.get('result'):
        return {'msg': admin.data.get('message'), 'code': 403}, 403
    form = ChangeUserPasswordForm(request.form)
    if form.validate():
        form_data = {key: form.data[key] for key in form.data if form.data[key]}
        user = AdminManager(form_data, handle_type='change_user_password')
        result, code = handle_route(user, del_redis_key='user')
        return jsonify(result), code
    return {'msg': get_error_message(form.errors), 'code': 403}, 403


@admin_bp.route('/modify_user_info', methods=["POST"])
@jwt_required()
def admin_modify_user_info():
    admin = AdminManager({'username': get_jwt_identity()}, handle_type='check_admin')
    if not admin.data.get('result'):
        return {'msg': admin.data.get('message'), 'code': 403}, 403
    form = ChangeUserInfoForm(request.form)
    if form.validate():
        form_data = {key: form.data[key] for key in form.data if form.data[key]}
        user = AdminManager(form_data, handle_type='modify_user_info')
        result, code = handle_route(user, del_redis_key='user')
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@admin_bp.route('/all_users', methods=["GET"])
@jwt_required()
def get_all_users():
    admin = AdminManager({'username': get_jwt_identity()}, handle_type='check_admin')
    if not admin.data.get('result'):
        return {'msg': admin.data.get('message'), 'code': 403}, 403
    form = GetAllUserForm(request.args)
    if form.validate():
        form_data = {key: form.data[key] for key in form.data if form.data[key]}
        page = str(form.page.data) if form.page.data else '1'
        redis_key = 'page_' + page + '_' + str(form_data.items()) + '_users'
        users_info = asyncio.run(get_value(redis_key))
        if users_info:
            return jsonify({'msg': 'success', 'data': eval(users_info), 'code': 200}), 200
        users = AdminManager(form_data, handle_type='get_all_users')
        result, code = handle_route(users, set_redis_key=redis_key)
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403
