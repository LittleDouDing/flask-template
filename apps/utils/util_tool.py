#!/usr/bin/env python
# -*- coding: utf-8 -*-
import apps
from apps.models import delete_key, get_keys, set_value
import asyncio
import re


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


def get_table_keys(table, not_contain_keys=None):
    regex = r'__.+|_sa_.+|' + '|'.join(not_contain_keys) if not_contain_keys else r'__.+|_sa_.+'
    return [key for key in list(table.__dict__.keys()) if not re.findall(regex, key)]
