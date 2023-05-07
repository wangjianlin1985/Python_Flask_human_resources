from flask import current_app, jsonify,g
from flask import render_template
from flask import request

from person import db
from person.utils.response_code import RET
from . import Superson
from person.models import Admin, SuperAdmin
from flask import session, redirect


@Superson.route("/")
def index():
    return render_template('index.html')


# 添加管理员数据
@Superson.route("/add_admin", methods=['POST'])
def add_admin():
    # 获取参数
    admin_id = request.json.get('admin_id')
    admin_psw = request.json.get('admin_psw')
    # 检查参数的完整性
    if not all([admin_id, admin_psw]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')
    # 校验是否int类型
    try:
        admin_id = int(admin_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数类型错误')


    # 构建模型类对象
    admin = Admin()
    admin.admin_id = admin_id
    admin.admin_psw = admin_psw
    # 存入数据库
    try:
        db.session.add(admin)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存数据失败')
        # 返回前端数据
    return jsonify(errno='0', errmsg='OK')

# 修改管理员数据
@Superson.route("/editor_admin", methods=['PUT'])
def editor_admin():
    # 获取参数
    admin_id_ = request.json.get('admin_id_')
    editor_admin_id = request.json.get('editor_admin_id')
    editor_admin_psw = request.json.get('editor_admin_psw')
    # 检查参数的完整性
    if not all([admin_id_, editor_admin_id, editor_admin_psw]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')
    # 校验是否int类型
    try:
        editor_admin_id = int(editor_admin_id)
        admin_id_ = int(admin_id_)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数类型错误')

    # 检查用户输入id和列表id是否一致
    if admin_id_ != editor_admin_id:
        return jsonify(errno=RET.DATAERR, errmsg='请输入正确要修改的管理员id错误')
    # 构建模型类对象
    try:
        admin = Admin.query.filter_by(admin_id=editor_admin_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询管理员错误')
    admin.admin_psw = editor_admin_psw
    # 存入数据库
    try:
        db.session.add(admin)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存数据失败')
        # 返回前端数据
    return jsonify(errno='0', errmsg='OK')

# 删除管理员数据
@Superson.route("/delete_admin", methods=['DELETE'])
def delete_admin():
    # 获取参数
    admin_id = request.json.get('admin_id')
    admin_psw = request.json.get('admin_psw')
    # 检查参数的完整性
    if not all([admin_id, admin_psw]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')
    # 校验是否int类型
    try:
        admin_id = int(admin_id)
        admin_psw = int(admin_psw)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数类型错误')
    # 构建模型类对象
    try:
        admin = Admin.query.filter_by(admin_id=admin_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询管理员错误')

    # 存入数据库
    try:
        db.session.delete(admin)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='删除数据失败')
        # 返回前端数据
    return jsonify(errno='0', errmsg='OK')


# 修改超级管理员密码
@Superson.route("/editor_superadminpsw", methods=['POST'])
def editor_superadminpsw():
    # 获取参数
    superadminpsw = request.json.get('superadminpsw')
    editorsuperadminpsw = request.json.get('editorsuperadminpsw')
    # 检查参数的完整性
    if not all([superadminpsw, editorsuperadminpsw]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')

    # 校验是否int类型
    try:
        superadminpsw = int(superadminpsw)
        editorsuperadminpsw = int(editorsuperadminpsw)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数类型错误')

    # 检查用户输入id和列表id是否一致
    sessions = session.get('superadmin_psw')
    superadmin_psw = int(sessions)
    if superadmin_psw != superadminpsw:
        return jsonify(errno=RET.DATAERR, errmsg='请输入超级管理员旧密码')
    # 构建模型类对象
    try:
        superadmin = SuperAdmin.query.filter_by(superadmin_psw=superadminpsw).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询超级管理员错误')
    # 修改超级管理员密码
    superadmin.superadmin_psw = editorsuperadminpsw
    # 存入数据库
    try:
        db.session.add(superadmin)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='修改密码失败')
    session.pop('superadmin_id', None)
    session.pop('superadmin_psw', None)
    # 返回前端数据
    return jsonify(errno='0', errmsg='OK')


# 退出超级管理员登录
@Superson.route("/exit_superadminpsw", methods=['POST'])
def exit_superadminpsw():
    session.pop('superadmin_id', None)
    session.pop('superadmin_psw', None)
    return jsonify(errno='0', errmsg='OK')

# 显示管理员列表数据
@Superson.route("/Superson.html")
def Supersons():
    try:
        # 获取用户状态保持信息
        superadmin_id = session['superadmin_id']
        superadmin_psw = session['superadmin_psw']
    except Exception as e:
        current_app.logger.error(e)
        return render_template('index.html')

    # 从数据库获取数据
    try:
        admins = Admin.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询管理员数据失败')
    # 判断查询结果
    if not admins:
        return jsonify(errno=RET.NODATA, errmsg='无管理员数据')
    # 定义列表，存储数据
    data = {
        'admins': admins
    }
    return render_template('Superson.html', data=data)
