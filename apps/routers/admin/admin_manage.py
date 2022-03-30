from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from apps.validates.admin_validate import AddUserForm, GetAllUserForm, DeleteUserForm, ChangeUserPasswordForm, \
    ChangeUserInfoForm
from apps.models.admin import AdminManager
from apps.utils.util_tool import get_error_message
from apps.models import set_value, get_value,delete_key
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
        message = user.data.get('message')
        if not user.data.get('result'):
            return jsonify({'msg': message, 'code': 403}), 403
        return jsonify({'msg': message, 'code': 200}), 200
    message = get_error_message(form.errors)
    return jsonify({'msg': message, 'code': 403}), 403


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
        message = user.data.get('message')
        if user.data.get('result'):
            return {'msg': message, 'code': 200}, 200
        asyncio.run(delete_key(form_data.get('username')))
        return {'msg': message, 'code': 403}, 403
    message = get_error_message(form.errors)
    return {'msg': message, 'code': 403}, 403


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
        message = user.data.get('message')
        if user.data.get('result'):
            return jsonify({'msg': message, 'code': 200}), 200
        return jsonify({'msg': message, 'code': 403}), 403
    message = get_error_message(form.errors)
    return {'msg': message, 'code': 403}, 403


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
        message = user.data.get('message')
        if user.data.get('result'):
            return jsonify({'msg': message, 'code': 200}), 200
        asyncio.run(delete_key(form_data.get('username')))
        return jsonify({'msg': message, 'code': 403}), 403
    message = get_error_message(form.errors)
    return jsonify({'msg': message, 'code': 403}), 403


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
        users_info = asyncio.run(get_value('page_' + page + '_' + str(form_data.items()) + '_users'))
        if users_info:
            return jsonify({'msg': 'success', 'data': eval(users_info), 'code': 200}), 200
        users = AdminManager(form_data, handle_type='get_all_users')
        message = users.data.get('message')
        if users.data.get('result'):
            data = users.data.get('data')
            asyncio.run(set_value('page_' + page + '_' + str(form_data.items()) + '_users', str(data)))
            return jsonify({'msg': message, 'data': data, 'code': 200}), 200
        return jsonify({'msg': message, 'code': 403}), 403
    message = get_error_message(form.errors)
    return jsonify({'msg': message, 'code': 403}), 403
