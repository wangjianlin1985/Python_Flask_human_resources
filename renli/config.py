# 导入redis模块
from redis import StrictRedis

class Config:
    DEBUG = None
    # 基本数据库的配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/test_project1'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 抽取redis的主机和端口号
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # 状态保持的基本配置
    SECRET_KEY = 'stPkMpYjBvYF26UsrwxR898oyasgdbX853nOjShiIBZoCHzYKI76cpaRUzdU'
    SESSION_TYPE = 'redis'
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 86400

# 定义开发模式下的配置类
class DevelopmentConfig(Config):
    DEBUG = True


# 定义生产模式下的配置类
class ProductionConfig(Config):
    DEBUG = False

# 定义字典，实现动态的加载不同的配置类
config_dict = {
    'development':DevelopmentConfig,
    'production':ProductionConfig
}