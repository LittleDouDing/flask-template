#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from extend import mail
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
from apps.models import delete_key, get_keys, set_value, get_value
from flask import make_response
from datetime import datetime
from hashlib import sha512
from os.path import dirname, join
import asyncio
import json
import uuid
import re
from io import BytesIO
import random
import string
from PIL import Image, ImageFont, ImageDraw


def validate_value(form_list, table):
    form_list = handle_form_data(form_list)
    table_form = get_table_form(table)
    form = table_form(ImmutableMultiDict(form_list))
    if not form.validate():
        return get_error_message(form.errors)


def get_table_id(table):
    table_keys = table.__dict__.keys()
    for key in table_keys:
        if '_id' in key:
            return key


def check_illegal_data(request_data):
    file_path = join(dirname(dirname(dirname(__file__))), 'xss_filter.json')
    with open(file_path, encoding='utf-8') as fp:
        result = json.load(fp)
        xss_filter = result['filter']
        filter_reg = r'|'.join(xss_filter)
        res = re.search(filter_reg, str(request_data))
        if res and res.group():
            return True
        return False


def encrypt_password(password):
    new_pwd = (password + 'XXXXXXXX').encode('utf-8')
    return sha512(new_pwd).hexdigest()


def get_conditions(datadict, table):
    return (table.__dict__.get(k).like('%' + datadict.get(k) + '%') for k in list(datadict) if
            k not in ['page', 'limit'])


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
            data_dict[key] = str(form.data[key]).strip()
        else:
            data_dict[key] = form.data[key]
    return data_dict


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
    regex = r'__.+|_sa_.+|.+_$|.+\d$'
    regex = r'|'.join(not_contain_keys) + '|' + regex if not_contain_keys else regex
    return [key for key in list(table.__dict__.keys()) if not re.findall(regex, key)]


def get_database_err(e):
    err_msg = str(e.args[0]).replace('\\', '')
    if 'Data too long' in err_msg:
        params = re.findall(r".+'(.+)'.+", err_msg)[0]
        err_msg = re.sub(r"column '(.+)'", e.__dict__.get('params')[params], err_msg)
    if 'Duplicate' in err_msg:
        params = re.findall(r".+for key '(.+)'", err_msg)[0]
        err_msg = '(pymysql.err.IntegrityError) (1062, Duplicate key for ' + params + ')'
    if 'foreign key' in err_msg:
        err_msg = 'To trigger a foreign key constraint, please ensure that the record exists in the main table'
    return err_msg


def add_new_access_week():
    this_week = {'Mon': 0, 'Tue': 0, 'Wed': 0, 'Thu': 0, 'Fri': 0, 'Sat': 0, 'Sun': 0}
    asyncio.run(set_value('this_week_access', str(this_week), expire=604800))


def handle_access_week():
    week_dict = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
    weekday = datetime.now().weekday()
    this_week = asyncio.run(get_value('this_week_access'))
    if this_week:
        this_week = eval(this_week)
        this_week[week_dict[weekday]] += 1
    asyncio.run(set_value('this_week_access', str(this_week), expire=604800))


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
        # # 把buf_str作为response返回前端，并设置首部字段
        response = make_response(buf_str)
        response.headers['Content-Type'] = 'image/png'
        # 将验证码字符串储存在redis中
        asyncio.run(set_value(self.image_id, code, expire=120))
        return response
