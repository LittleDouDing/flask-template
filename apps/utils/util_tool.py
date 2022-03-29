#!/usr/bin/env python
# -*- coding: utf-8 -*-
import apps
from apps.models import db

session = db.session


class Pager:
    def __init__(self, current_page, per_items=20):
        self.current_page = current_page
        # 规定每一页的个数
        self.per_items = per_items

    @property
    def start(self):
        val = (self.current_page - 1) * self.per_items
        return val

    @property
    def end(self):
        val = self.current_page * self.per_items
        return val


def get_error_message(errors):
    return ';'.join([';'.join(errors.get(key)) for key in errors])


def send_async_email(msg):
    import app
    with app.app.app_context():
        apps.mail.send(msg)
