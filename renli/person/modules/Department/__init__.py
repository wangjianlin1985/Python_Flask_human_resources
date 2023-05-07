from flask import Blueprint

Departments = Blueprint('Departments',__name__)

# 把使用蓝图对象的文件导入到创建蓝图对象下面
from . import views