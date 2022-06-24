import asyncio
import os
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from apps.models import get_value
from flask import request, current_app
from apps.utils.util_tool import random_filename
from flask_jwt_extended import get_jwt
from flask_jwt_extended import verify_jwt_in_request


def permission_required(permission_name):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get('author') != permission_name:
                return {'msg': 'The current user does not have permission to perform this operation', 'code': 403}, 403
            return fn(*args, **kwargs)

        return decorator

    return wrapper


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if not claims.get('is_admin'):
                return {'msg': 'Only administrators can perform this operation', 'code': 403}, 403
            return fn(*args, **kwargs)

        return decorator

    return wrapper


def current_user_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            username = request.form.get('username') if request.form.get('username') else request.args.get('username')
            if username != get_jwt_identity():
                return {'msg': 'Only the current user can perform this operation', 'code': 403}, 403
            return fn(*args, **kwargs)

        return decorator

    return wrapper


def random_code_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            image_id = request.form.get('image_id')
            random_code = asyncio.run(get_value(image_id))
            img_code = request.form.get('img_code')
            if not random_code or random_code.lower() != img_code.lower():
                return {'msg': 'The verification code is expired or incorrect', 'code': 403}, 403
            return fn(*args, **kwargs)

        return decorator

    return wrapper


def email_code_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            email_code = request.form.get('email_code')
            usertype = 'user' if '/user/' in request.url else 'admin'
            if usertype == 'admin':
                if not asyncio.run(get_value('random_code')):
                    return {'msg': "The email verification code has expired", 'code': 403}, 403
                if email_code != asyncio.run(get_value('random_code')):
                    return {'msg': "The email verification code input error", 'code': 403}, 403
            return fn(*args, **kwargs)

        return decorator

    return wrapper


def file_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            uploaded_file = request.files.get('file')
            if not uploaded_file:
                return {'msg': 'Please upload excel file', 'code': 403}, 403
            new_filename = random_filename(uploaded_file.filename)
            if new_filename:
                file_ext = os.path.splitext(new_filename)[1]
                if file_ext in current_app.config.get('UPLOAD_EXTENSIONS'):
                    return fn(*args, **kwargs)
                return {'msg': 'The file format does not conform to specification', 'code': 403}, 403

        return decorator

    return wrapper


def times_limited(limit_type):
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            username = request.form.get('username')
            if limit_type == 'modify_info_num':
                modify_info_num = asyncio.run(get_value(username + '_modify_info_num'))
                if modify_info_num and int(modify_info_num) >= 10:
                    return {'msg': 'Too many modify information times, please try again in 3 hours', 'code': 403}, 403
            if limit_type == 'change_pwd_num':
                change_pwd_num = asyncio.run(get_value(username + '_change_pwd_num'))
                if change_pwd_num and int(change_pwd_num) >= 10:
                    return {'msg': 'Too many change password times, please try again in 6 hours', 'code': 403}, 403
            if limit_type == 'error_num':
                error_num = asyncio.run(get_value(username + '_error_num'))
                if error_num and int(error_num) >= 5:
                    return {'msg': 'Too many login errors, please try again in 30 minutes', 'code': 403}, 403
            if limit_type == 'login_num':
                login_num = asyncio.run(get_value(username + '_login_num'))
                if login_num and int(login_num) >= 10:
                    return {'msg': 'Too many login times, please try again in 6 hours', 'code': 403}, 403
            return func(*args, **kwargs)

        return decorator

    return wrapper
