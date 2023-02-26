#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_cors import CORS
from apps import create_app
from warnings import filterwarnings

filterwarnings('ignore')
app = create_app()

if __name__ == '__main__':
    CORS(app)
    app.run(host='0.0.0.0', port=5000)
