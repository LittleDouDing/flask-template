from flask import Flask
from setting import ProductionConfig
from apps.routers import general_bp, admin_bp, device_bp, network_bp, port_bp, topology_bp
from apps.models import db
from flask_mail import Mail
from flask_jwt_extended import JWTManager

mail = Mail()


def create_app():
    app = Flask(__name__)
    # 加载配置
    app.config.from_object(ProductionConfig())
    # 添加flask-sqlalchemy配置
    db.init_app(app)
    mail.init_app(app)
    JWTManager(app)
    # 注册蓝图
    app.register_blueprint(general_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(device_bp)
    app.register_blueprint(network_bp)
    app.register_blueprint(port_bp)
    app.register_blueprint(topology_bp)
    return app
