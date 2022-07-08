from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from apps.utils.util_tool import get_error_message, get_form_data
from apps.utils.route_tool import handle_route
from apps.models import get_value, delete_key, set_times, set_value
from apps.database.general import UserManager
from apps.validates.general_validate import GetInformationFrom, LoginFrom, ChangeUserPasswordForm, ModifyInfoForm, \
    ChangeAdminPasswordForm
from decorators import current_user_required, times_limited, random_code_required, email_code_required
import asyncio

general_bp = Blueprint('general_data', __name__, url_prefix='/api/v1')


@general_bp.route('/admin/information', methods=['GET'])
@general_bp.route('/user/information', methods=['GET'])
@current_user_required()
@jwt_required()
def get_user_info():
    usertype = 'user' if '/user/' in request.url else 'admin'
    # 参数username
    form = GetInformationFrom(request.args)
    if form.validate():
        user_info = asyncio.run(get_value(form.username.data + '_user_info'))
        if user_info:
            return jsonify({'msg': 'success', 'data': eval(user_info), 'code': 200}), 200
        user = UserManager(get_form_data(form), usertype=usertype, handle_type='get_info')
        result, code = handle_route(user, set_redis_key=form.username.data + '_user_info')
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@general_bp.route('/admin/login', methods=['POST'])
@general_bp.route('/user/login', methods=['POST'])
# @random_code_required()
@times_limited(limit_type='error_num')
@times_limited(limit_type='login_num')
def user_login():
    usertype = 'user' if '/user/' in request.url else 'admin'
    # 参数username， password
    form = LoginFrom(request.form)
    if form.validate():
        image_id = form.image_id.data
        ip_address = request.remote_addr
        form_data = get_form_data(form)
        user = UserManager(form_data, usertype=usertype, handle_type='user_login')
        if user.data.get('result'):
            asyncio.run(delete_key(form_data.get('username') + '_error_num'))
            asyncio.run(set_times(form_data.get('username') + '_login_num', expire=21600))
            asyncio.run(delete_key(image_id))
            asyncio.run(set_value(ip_address, form.username.data, expire=1800))
            is_admin, author = user.data.get('is_admin'), user.data.get('author')
            access_token = create_access_token(
                identity=form.username.data, additional_claims={'author': author, 'is_admin': is_admin}
            )
            return jsonify({'msg': user.data.get('message'), 'token': access_token, 'code': 200}), 200
        asyncio.run(set_times(form_data.get('username') + '_error_num'))
        return jsonify({'msg': user.data.get('message'), 'code': 403}), 403
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@general_bp.route('/admin/change_password', methods=['POST'])
@general_bp.route('/user/change_password', methods=['POST'])
@times_limited(limit_type='change_pwd_num')
@email_code_required()
@current_user_required()
@jwt_required()
def change_password():
    usertype = 'user' if '/user/' in request.url else 'admin'
    # 参数username, old_password, new_password
    if usertype == 'admin':
        form = ChangeAdminPasswordForm(request.form)
    else:
        form = ChangeUserPasswordForm(request.form)
    if form.validate():
        redis_key = form.username.data + '_change_pwd_num'
        user = UserManager(get_form_data(form), usertype=usertype, handle_type='modify_password')
        result, code = handle_route(user)
        asyncio.run(set_times(redis_key, expire=21600)) if code == 200 else None
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@general_bp.route('/admin/modify_info', methods=['POST'])
@general_bp.route('/user/modify_info', methods=['POST'])
@times_limited(limit_type='modify_info_num')
@current_user_required()
@jwt_required()
def modify_info():
    usertype = 'user' if '/user/' in request.url else 'admin'
    # 参数username, old_password, new_password
    form = ModifyInfoForm(request.form)
    if form.validate():
        redis_key = form.username.data + '_modify_info_num'
        user = UserManager(get_form_data(form), usertype=usertype, handle_type='modify_info')
        result, code = handle_route(user, del_redis_key='user')
        asyncio.run(set_times(redis_key, expire=10800)) if code == 200 else None
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@general_bp.route('/user/logout', methods=['POST'])
@general_bp.route('/admin/logout', methods=['POST'])
@jwt_required()
def user_logout():
    ip_address = request.remote_addr
    username = asyncio.run(get_value(ip_address))
    if username == get_jwt_identity():
        asyncio.run(delete_key(ip_address))
        return {'msg': 'The user logout successfully', 'code': 200}, 200
    return {'msg': 'The user logout failed', 'code': 403}, 403

