from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from apps.utils.util_tool import get_error_message, send_async_email
from apps.models import set_value, get_value, set_error, delete_key
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
            return jsonify({'msg': "Only the information of the current user can be manipulated", 'code': 403}), 403
        # 从redis中获取数据
        user_info = asyncio.run(get_value(username))
        if user_info:
            return jsonify({'msg': 'success', 'data': eval(user_info), 'code': 200}), 200
        form_data = {key: form.data[key] for key in form.data if form.data[key]}
        user = UserManager(form_data, usertype=usertype, handle_type='get_info')
        message = user.data.get('message')
        if user.data.get('result'):
            asyncio.run(set_value(username, str(user.data.get('data'))))
            return jsonify({'msg': message, 'data': user.data.get('data'), 'code': 200}), 200
        return jsonify({'msg': message, 'code': 403}), 403
    message = get_error_message(form.errors)
    return jsonify({'msg': message, 'code': 403}), 403


@general_bp.route('/admin/login', methods=['POST'])
@general_bp.route('/user/login', methods=['POST'])
def user_login():
    usertype = 'user' if '/user/' in request.url else 'admin'
    error_num = asyncio.run(get_value(request.form.get('username') + '_error_num'))
    if error_num and int(error_num) >= 3:
        error = 'The maximum number of errors has been reached, please try again in 30 minutes'
        return jsonify({'msg': error, 'code': 403}), 403
    # 参数username， password
    form = LoginFrom(request.form)
    if form.validate():
        form_data = {key: form.data[key] for key in form.data if form.data[key]}
        user = UserManager(form_data, usertype=usertype, handle_type='check_user')
        message = user.data.get('message')
        # 查找到该用户
        if user.data.get('result'):
            username = form.username.data
            asyncio.run(delete_key(form_data.get('username') + '_error_num'))
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            return jsonify({'msg': message, 'token': access_token, 'refresh_token': refresh_token, 'code': 200}), 200
        asyncio.run(set_error(form_data.get('username') + '_error_num'))
        return jsonify({'msg': message, 'code': 403}), 403
    message = get_error_message(form.errors)
    return jsonify({'msg': message, 'code': 403}), 403


@general_bp.route('/admin/change_password', methods=['POST'])
@general_bp.route('/user/change_password', methods=['POST'])
@jwt_required()
def change_password():
    usertype = 'user' if '/user/' in request.url else 'admin'
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
            return jsonify({'msg': "Only the information of the current user can be manipulated", 'code': 403}), 403
        form_data = {key: form.data[key] for key in form.data if form.data[key]}
        user = UserManager(form_data, usertype=usertype, handle_type='modify_password')
        message = user.data.get('message')
        if user.data.get('result'):
            return jsonify({'msg': message, 'code': 200}), 200
        return jsonify({'msg': message, 'code': 403}), 403
    message = get_error_message(form.errors)
    return jsonify({'msg': message, 'code': 403}), 403


@general_bp.route('/admin/modify_info', methods=['POST'])
@general_bp.route('/user/modify_info', methods=['POST'])
@jwt_required()
def modify_info():
    usertype = 'user' if '/user/' in request.url else 'admin'
    # 参数username, old_password, new_password
    form = ModifyInfoForm(request.form)
    if form.validate():
        if form.username.data != get_jwt_identity():
            return jsonify({'msg': "Only the information of the current user can be manipulated", 'code': 403}), 403
        form_data = {key: form.data[key] for key in form.data if form.data[key]}
        user = UserManager(form_data, usertype=usertype, handle_type='modify_info')
        message = user.data.get('message')
        if not user.data.get('result'):
            return jsonify({'msg': message, 'code': 406}), 403
        asyncio.run(delete_key(form_data.get('username')))
        return jsonify({'msg': message, 'code': 200}), 200
    message = get_error_message(form.errors)
    return jsonify({'msg': message, 'code': 403}), 403
