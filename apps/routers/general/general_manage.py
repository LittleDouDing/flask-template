from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from apps.utils.util_tool import get_error_message, send_async_email, get_form_data, handle_route, ImageCode
from apps.models import set_value, get_value, delete_key, set_times
from apps.models.general import UserManager
from apps.validates.general_validate import GetInformationFrom, LoginFrom, ChangeUserPasswordForm, ModifyInfoForm, \
    ChangeAdminPasswordForm
from flask_mail import Message
from threading import Thread
import string
import random
import asyncio

general_bp = Blueprint('general_data', __name__, url_prefix='/api/v1')


@general_bp.route("/refresh", methods=["GET"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(refresh_token=access_token)


@general_bp.route("/send_email", methods=["GET"])
def send_email():
    random_code = ''.join(random.sample(string.digits, 6))
    header = 'Email verification code'
    body = 'The current verification code is：' + random_code + '（Valid for 2 minutes）'
    msg = Message(header, recipients=['1693536530@qq.com'], body=body)
    thread = Thread(target=send_async_email, args=[msg])
    thread.start()
    asyncio.run(set_value('random_code', str(random_code), expire=120))
    return jsonify({'msg': 'Email verification code sent successfully', 'code': 200}), 200


@general_bp.route('/get_code')
def get_random_code():
    return ImageCode().get_img_code()


@general_bp.app_errorhandler(404)
def page_unauthorized(error):
    return jsonify({'msg': 'The page you are currently visiting does not exist', 'code': 404}), 404


@general_bp.route('/admin/information', methods=['GET'])
@general_bp.route('/user/information', methods=['GET'])
@jwt_required()
def get_user_info():
    usertype = 'user' if '/user/' in request.url else 'admin'
    # 参数username
    form = GetInformationFrom(request.args)
    if form.validate():
        username = form.username.data
        if username != get_jwt_identity():
            return jsonify({'msg': 'Only the information of the current user can be manipulated', 'code': 403}), 403
        user_info = asyncio.run(get_value(username + '_user_info'))
        if user_info:
            return jsonify({'msg': 'success', 'data': eval(user_info), 'code': 200}), 200
        user = UserManager(get_form_data(form), usertype=usertype, handle_type='get_info')
        result, code = handle_route(user, set_redis_key=username + '_user_info')
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@general_bp.route('/admin/login', methods=['POST'])
@general_bp.route('/user/login', methods=['POST'])
def user_login():
    usertype = 'user' if '/user/' in request.url else 'admin'
    error_num = asyncio.run(get_value(request.form.get('username') + '_error_num'))
    login_num = asyncio.run(get_value(request.form.get('username') + '_login_num'))
    if error_num and int(error_num) >= 3:
        return jsonify({'msg': 'Too many login errors, please try again in 30 minutes', 'code': 403}), 403
    if login_num and int(login_num) >= 6:
        return jsonify({'msg': 'Too many login times, please try again in 6 hours', 'code': 403}), 403
    # 参数username， password
    form = LoginFrom(request.form)
    if form.validate():
        form_data = get_form_data(form)
        random_code = asyncio.run(get_value('image_code'))
        if not random_code or random_code.lower() != form_data.get('img_code').lower():
            return jsonify({'msg': 'The verification code is expired or incorrect', 'code': 403}), 403
        user = UserManager(form_data, usertype=usertype, handle_type='user_login')
        if user.data.get('result'):
            asyncio.run(delete_key(form_data.get('username') + '_error_num'))
            asyncio.run(set_times(form_data.get('username') + '_login_num', expire=21600))
            access_token = create_access_token(identity=form.username.data)
            return jsonify({'msg': user.data.get('message'), 'token': access_token, 'code': 200}), 200
        asyncio.run(set_times(form_data.get('username') + '_error_num'))
        return jsonify({'msg': user.data.get('message'), 'code': 403}), 403
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@general_bp.route('/admin/change_password', methods=['POST'])
@general_bp.route('/user/change_password', methods=['POST'])
@jwt_required()
def change_password():
    usertype = 'user' if '/user/' in request.url else 'admin'
    redis_key = request.form.get('username') + '_change_pwd_num'
    change_pwd_num = asyncio.run(get_value(redis_key))
    if change_pwd_num and int(change_pwd_num) >= 5:
        return jsonify({'msg': 'Too many change password times, please try again in 6 hours', 'code': 403}), 403
    # 参数username, old_password, new_password
    if usertype == 'admin':
        form = ChangeAdminPasswordForm(request.form)
    else:
        form = ChangeUserPasswordForm(request.form)
    if form.validate():
        if usertype == 'admin':
            if not asyncio.run(get_value('random_code')):
                return jsonify({'msg': "The email verification code has expired", 'code': 403}), 403
            if form.email_code.data != asyncio.run(get_value('random_code')):
                return jsonify({'msg': "The email verification code input error", 'code': 403}), 403
        if form.username.data != get_jwt_identity():
            return jsonify({'msg': 'Only the information of the current user can be manipulated', 'code': 403}), 403
        user = UserManager(get_form_data(form), usertype=usertype, handle_type='modify_password')
        result, code = handle_route(user)
        asyncio.run(set_times(redis_key, expire=21600)) if code == 200 else None
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403


@general_bp.route('/admin/modify_info', methods=['POST'])
@general_bp.route('/user/modify_info', methods=['POST'])
@jwt_required()
def modify_info():
    usertype = 'user' if '/user/' in request.url else 'admin'
    redis_key = request.form.get('username') + '_modify_info'
    modify_info_num = asyncio.run(get_value(redis_key))
    if modify_info_num and int(modify_info_num) >= 10:
        return jsonify({'msg': 'Too many modify information times, please try again in 3 hours', 'code': 403}), 403
    # 参数username, old_password, new_password
    form = ModifyInfoForm(request.form)
    if form.validate():
        if form.username.data != get_jwt_identity():
            return jsonify({'msg': 'Only the information of the current user can be manipulated', 'code': 403}), 403
        user = UserManager(get_form_data(form), usertype=usertype, handle_type='modify_info')
        result, code = handle_route(user, del_redis_key='user')
        asyncio.run(set_times(redis_key, expire=10800)) if code == 200 else None
        return jsonify(result), code
    return jsonify({'msg': get_error_message(form.errors), 'code': 403}), 403
