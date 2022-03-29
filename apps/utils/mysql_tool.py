#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib import parse
import os

PASSWORD = parse.quote_plus("Lin123456@")
STRING = f'sqlacodegen mysql+pymysql://root:{PASSWORD}@127.0.0.1:3306/ledgersystem > models.py'
res = os.popen(STRING)
print(res)
