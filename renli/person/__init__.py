from flask import Flask
# 使用flask_session扩展包
from flask_session import Session
# 导入flask_sqlalchemy扩展
from flask_sqlalchemy import SQLAlchemy
from config import config_dict, Config
# 导入日志模块和日志文件处理模块
import logging
from logging.handlers import RotatingFileHandler
from redis import StrictRedis

# 导入flask_wtf扩展包，为了e给服务器开启csrf保护和验证
from flask_wtf import CSRFProtect, csrf

db = SQLAlchemy()
redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)

# from werkzeug.security import generate_password_hash,check_password_hash



# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG)  # 调试debug级
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
# 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式m6
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日志记录器
logging.getLogger().addHandler(file_log_handler)


# 定义工厂函数，作用：封装创建程序实例的功能代码，让工厂函数能够根据参数的不同，生产不同环境下的app
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])
    # 实例化sqlalchemy对象
    # db = SQLAlchemy(app)
    db.init_app(app)
    # 实例化Session对象
    Session(app)
    # 开启csrf保护
    CSRFProtect(app)

    # 生成csrf_token口令，返回给客户端浏览器的cookie中
    # 使用请求勾子(中间件)，在每次请求后，把csrf_token写入客户端的cookie中
    @app.after_request
    def after_request(response):
        csrf_token = csrf.generate_csrf()
        response.set_cookie('csrf_token', csrf_token)  # 把csrf_token设置到浏览器的Set-cookie
        return response

    # 导入蓝图对象

    from person.modules.Admin import Admin
    app.register_blueprint(Admin)

    from person.modules.AdminLogin import AdminLogin
    app.register_blueprint(AdminLogin)

    from person.modules.Department import Departments
    app.register_blueprint(Departments)

    from person.modules.Resource import Resource
    app.register_blueprint(Resource)

    from person.modules.Rewards import Rewards
    app.register_blueprint(Rewards)

    from person.modules.SuperadminLogin import SuperadminLogin
    app.register_blueprint(SuperadminLogin)

    from person.modules.Superson import Superson
    app.register_blueprint(Superson)

    from person.modules.AdminChoose import AdminChoose
    app.register_blueprint(AdminChoose)

    return app
