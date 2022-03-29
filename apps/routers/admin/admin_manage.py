from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from apps.validates.admin_validate import AddUserForm, GetAllUserForm, DeleteUserForm, ChangeUserPasswordForm, \
    ChangeUserInfoForm
from apps.models.admin import AdminManager
from apps.utils.util_tool import get_error_message
from apps.models import set_value, get_value
import asyncio

admin_bp = Blueprint('admin_data', __name__, url_prefix='/api/v1/admin')


@admin_bp.route('/add_user', methods=["POST"])
@jwt_required()
def admin_add_user():
    form = AddUserForm(request.form)
    if form.validate():
        user = AdminManager(request.form, handle_type='add_user')
        message = user.data.get('message')
        if not user.data.get('result'):
            return jsonify({'msg': message, 'code': 403}), 403
        return jsonify({'msg': message, 'code': 200}), 200
    message = get_error_message(form.errors)
    return jsonify({'msg': message, 'code': 403}), 403


@admin_bp.route('/delete_user', methods=["POST"])
@jwt_required()
def admin_delete_user():
    form = DeleteUserForm(request.form)
    if form.validate():
        user = AdminManager(request.form, handle_type='delete_user')
        message = user.data.get('message')
        if user.data.get('result'):
            return {'msg': message, 'code': 200}, 200
        return {'msg': message, 'code': 403}, 403
    message = get_error_message(form.errors)
    return {'msg': message, 'code': 403}, 403


@admin_bp.route('/change_user_password', methods=["POST"])
@jwt_required()
def admin_change_user_password():
    form = ChangeUserPasswordForm(request.form)
    if form.validate():
        user = AdminManager(request.form, handle_type='change_user_password')
        message = user.data.get('message')
        if user.data.get('result'):
            return jsonify({'msg': message, 'code': 200}), 200
        return jsonify({'msg': message, 'code': 403}), 403
    message = get_error_message(form.errors)
    return {'msg': message, 'code': 403}, 403


@admin_bp.route('/modify_user_info', methods=["POST"])
@jwt_required()
def admin_modify_user_info():
    form = ChangeUserInfoForm(request.form)
    if form.validate():
        user = AdminManager(request.form, handle_type='modify_user_info')
        message = user.data.get('message')
        if user.data.get('result'):
            return jsonify({'msg': message, 'code': 200}), 200
        return jsonify({'msg': message, 'code': 403}), 403
    message = get_error_message(form.errors)
    return jsonify({'msg': message, 'code': 403}), 403


@admin_bp.route('/all_users', methods=["GET"])
@jwt_required()
def get_all_users():
    form = GetAllUserForm(request.args)
    if form.validate():
        page = str(form.page.data) if form.page.data else '1'
        users_info = asyncio.run(get_value('page_' + page + '_users'))
        if users_info:
            return jsonify({'msg': 'success', 'data': eval(users_info), 'code': 200}), 200
        users = AdminManager(request.args, handle_type='all_users')
        message = users.data.get('message')
        if users.data.get('result'):
            data = users.data.get('data')
            asyncio.run(set_value('page_' + page + '_users', str(data)))
            return jsonify({'msg': message, 'data': data, 'code': 200}), 200
        return jsonify({'msg': message, 'code': 403}), 403
    message = get_error_message(form.errors)
    return jsonify({'msg': message, 'code': 403}), 403
