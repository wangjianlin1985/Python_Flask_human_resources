# 导入flask_migrate扩展和script扩展
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
# 从info目录下导入db，app
from person import create_app,db,models
from person.models import SuperAdmin
# from person.models import User
# 调用工厂函数创建应用实例再启动
app = create_app('development')

# 实例化管理对象
manage = Manager(app)
# 数据库迁移
Migrate(app,db)
# 添加迁移命令
manage.add_command("db",MigrateCommand)

"""
迁移步骤：
1、创建迁移仓库
python manage.py db init 
2、创建迁移脚本
python manage.py db migrate -m 'init_tables'
3、执行迁移脚本
python manage.py db upgrade 

迁移脚本不成功：在manage.py文件中导入models

"""
# python manage.py create_supperuser -n 用户名 -p 密码
# python manage.py create_supperuser -n 1 -p 123456
@manage.option('-n', '-superadmin_id', dest='superadmin_id')
@manage.option('-p', '-superadmin_psw', dest='superadmin_psw')
def create_supperuser(superadmin_id, superadmin_psw):
    if not all([superadmin_id, superadmin_psw]):
        print('参数缺失')
    superadmin = SuperAdmin()
    superadmin.superadmin_id = superadmin_id
    superadmin.superadmin_psw =superadmin_psw
    try:
        db.session.add(superadmin)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
    print('超级管理员创建成功')

if __name__ == '__main__':
    manage.run()
