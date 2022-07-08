#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from extend import mail
from werkzeug.utils import secure_filename
from apps.models import delete_key, get_keys, set_value
from flask import make_response
import asyncio
import uuid
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
        mail.send(msg)


def delete_relate_keys(relate_key):
    for key in asyncio.run(get_keys()):
        asyncio.run(delete_key(key)) if relate_key in key else None


def get_form_data(form):
    data_dict = {}
    for key in form.data:
        if form.data[key] and type(form.data[key]) == str or type(form.data[key]) == list:
            data_dict[key] = str(form.data[key]).replace("'", '"').strip()
        else:
            data_dict[key] = form.data[key]
    return data_dict
    # return {key: form.data[key] for key in form.data if form.data[key]}


def check_uuid(image_id):
    try:
        return uuid.UUID(image_id).version in [1, 2, 3, 4]
    except ValueError:
        return False


def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    filename = secure_filename(new_filename)
    return filename


def get_table_keys(table, not_contain_keys=None):
    regex = r'device_topology|device_account|__.+|_sa_.+|.+_$|.+\d$'
    regex = r'|'.join(not_contain_keys) + '|' + regex if not_contain_keys else regex
    return [key for key in list(table.__dict__.keys()) if not re.findall(regex, key)]


def get_database_err(e):
    err_msg = str(e.args[0]).replace('\\', '')
    if 'Data too long' in err_msg:
        params = re.findall(r".+'(.+)'.+", err_msg)[0]
        err_msg = re.sub(r"column '(.+)'", e.__dict__.get('params')[params], err_msg)
    if 'Duplicate' in err_msg:
        params = re.findall(r".+'(.+)'.+'.+'", err_msg)[0]
        err_msg = '(pymysql.err.IntegrityError) (1062, Duplicate key for ' + params + ')'
    if 'foreign key' in err_msg:
        err_msg = 'To trigger a foreign key constraint, please ensure that the record exists in the main table'
    return err_msg


class ImageCode:
    def __init__(self, image_id):
        self.image_id = image_id

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
        asyncio.run(set_value(self.image_id, code, expire=120))
        return response
