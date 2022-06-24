from flask import Flask, Blueprint
from setting import DevelopmentConfig
from middlewares import handle_before_request
from extend import limiter, mail
import flask_excel as excel
from apps.models import db
from flask_jwt_extended import JWTManager
from apps import routers
import pkgutil
import sys


def search_blueprint(app: Flask):
    app_dict = {}
    pkg_list = pkgutil.walk_packages(routers.__path__, routers.__name__ + ".")
    for _, module_name, is_pkg in pkg_list:
        __import__(module_name)
        module = sys.modules[module_name]
        module_attrs = dir(module)
        for name in module_attrs:
            var_obj = getattr(module, name)
            if isinstance(var_obj, Blueprint):
                if app_dict.get(name) is None:
                    app_dict[name] = var_obj
                    app.register_blueprint(var_obj)


def create_app():
    app = Flask(__name__, static_folder='./static')
    # 加载配置
    app.config.from_object(DevelopmentConfig())
    # 添加flask-sqlalchemy、mail、jwt、limiter、excel配置
    db.init_app(app)
    mail.init_app(app)
    JWTManager(app)
    limiter.init_app(app)
    excel.init_excel(app)
    # 处理中间件
    # app.before_request(handle_before_request)
    # 注册蓝图
    search_blueprint(app)
    return app
