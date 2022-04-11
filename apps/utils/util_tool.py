#!/usr/bin/env python
# -*- coding: utf-8 -*-
import apps
from apps.models import delete_key, get_keys, set_value
from apps.models.general import UserManager
from flask_jwt_extended import get_jwt_identity
from flask import make_response
import asyncio
import re
from io import BytesIO
import random
import string
from PIL import Image, ImageFont, ImageDraw


def get_error_message(errors):
    return ';'.join([';'.join(errors.get(key)) for key in errors])


def send_async_email(msg):
    import app
    with app.app.app_context():
        apps.mail.send(msg)


def delete_relate_keys(relate_key):
    for key in asyncio.run(get_keys()):
        asyncio.run(delete_key(key)) if relate_key in key else None


def get_form_data(form):
    return {key: form.data[key] for key in form.data if form.data[key]}


def handle_route(obj, set_redis_key=None, del_redis_key=None):
    message = obj.data.get('message')
    if obj.data.get('result'):
        asyncio.run(set_value(set_redis_key, str(obj.data.get('data')))) if set_redis_key else None
        delete_relate_keys(del_redis_key) if del_redis_key else None
        if obj.data.get('data'):
            return {'msg': obj.data.get('message'), 'data': obj.data.get('data'), 'code': 200}, 200
        return {'msg': message, 'code': 200}, 200
    return {'msg': message, 'code': 403}, 403


def get_user_author():
    user = UserManager(datadict={'username': get_jwt_identity()}, handle_type='get_author')
    return user.author


def get_table_keys(table, not_contain_keys=None):
    regex = r'__.+|_sa_.+|' + '|'.join(not_contain_keys) if not_contain_keys else r'__.+|_sa_.+'
    return [key for key in list(table.__dict__.keys()) if not re.findall(regex, key)]


def get_topology(result):
    topology = ''
    for index, item in enumerate(result['topology']):
        device, port = item.split(':')
        if index % 2 == 0:
            if device in topology:
                topology += '(' + port + ')'
            else:
                topology += device + '(' + port + ')'
        else:
            topology += '<----->' + '(' + port + ')' + device
    return topology


class ImageCode:
    @staticmethod
    def _rnd_color():
        # 随机颜色
        return random.randint(32, 127), random.randint(32, 127), random.randint(32, 127)

    @staticmethod
    def _gene_text():
        # 生成4位验证码 ascii_letters是生成所有字母 digits是生成所有数字0-9
        return ''.join(random.sample(string.ascii_letters + string.digits, 4))

    @staticmethod
    def _draw_lines(draw, num, width, height):
        # 划线
        for num in range(num):
            x1 = random.randint(0, width / 2)
            y1 = random.randint(0, height / 2)
            x2 = random.randint(0, width)
            y2 = random.randint(height / 2, height)
            x3 = random.randint(0, width)
            y3 = random.randint(height / 2, height)
            draw.line(((x1, y1), (x2, y2), (x3, y3)), fill='black', width=2)

    def _get_verify_code(self):
        # 生成验证码图形
        code = self._gene_text()
        # 图片大小120×50
        width, height = 120, 50
        # 新图片对象
        im = Image.new('RGB', (width, height), 'white')
        # 字体
        font = ImageFont.truetype('app/static/arial.ttf', 40)
        # draw对象
        draw = ImageDraw.Draw(im)
        # 绘制字符串
        for item in range(4):
            draw.text((5 + random.randint(-3, 3) + 23 * item, 5 + random.randint(-3, 3)),
                      text=code[item], fill=self._rnd_color(), font=font)
        # 划线
        self._draw_lines(draw, 5, width, height)
        return im, code

    def get_img_code(self):
        image, code = self._get_verify_code()
        # 图片以二进制形式写入
        buf = BytesIO()
        image.save(buf, 'jpeg')
        buf_str = buf.getvalue()
        # 把buf_str作为response返回前端，并设置首部字段
        response = make_response(buf_str)
        response.headers['Content-Type'] = 'image/gif'
        # 将验证码字符串储存在redis中
        asyncio.run(set_value('image_code', code, expire=120))
        return response
