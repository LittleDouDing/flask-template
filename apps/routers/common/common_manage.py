from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from apps.utils.util_tool import send_async_email, ImageCode, check_uuid
from apps.models import set_value
from extend import limiter
from flask_mail import Message
from threading import Thread
import string
import random
import asyncio

common_bp = Blueprint('common_data', __name__, url_prefix='/api/v1')


@common_bp.route("/refresh", methods=["GET"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(refresh_token=access_token)


@common_bp.route("/send_email", methods=["GET"])
@jwt_required()
@limiter.limit("10/minute")
def send_email():
    random_code = ''.join(random.sample(string.digits, 6))
    header = 'Email verification code'
    body = 'The current verification code is：' + random_code + '（Valid for 2 minutes）'
    msg = Message(header, recipients=['1693536530@qq.com'], body=body)
    thread = Thread(target=send_async_email, args=[msg])
    thread.start()
    asyncio.run(set_value('random_code', str(random_code), expire=120))
    return jsonify({'msg': 'Email verification code sent successfully', 'code': 200}), 200


@common_bp.route('/get_code')
@limiter.limit("60/minute")
def get_random_code():
    image_id = request.args.get('image_id')
    if not image_id:
        return {'msg': 'The image id cannot be empty', 'code': 403}, 403
    if not check_uuid(image_id):
        return {'msg': 'The image id is not a legal UUID', 'code': 403}, 403
    response = ImageCode(image_id=image_id).get_img_code()
    return response


@common_bp.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'error': "rate limit exceeded %s" % e.description}), 429


@common_bp.app_errorhandler(404)
def page_unauthorized(error):
    return jsonify({'msg': 'The page you are currently visiting does not exist', 'code': 404}), 404


@common_bp.app_errorhandler(413)
def file_too_large(error):
    return jsonify({'msg': 'The uploaded file exceeds the size limit', 'code': 413}), 413
