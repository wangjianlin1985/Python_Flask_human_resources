from flask import session,current_app,g
from person.models import User

# 工具包，让被装饰器装饰的函数的属性不发生变化
import functools

def login_required(f):
    @functools.wraps(f)
    def wrapper(*args,**kwargs):
        # 使用请求上下文对象session，从redis中获取用户id
        user_id = session.get("user_id")
        user = None
        # 如果user_id存在
        if user_id:
            # 查询mysql
            try:
                user = User.query.get(user_id)
            except Exception as e:
                current_app.logger.error(e)
        # 使用g对象，来临时存储获取的用户信息
        g.user = user
        return f(*args,**kwargs)
    # wrapper.__name__ = f.__name__
    return wrapper
