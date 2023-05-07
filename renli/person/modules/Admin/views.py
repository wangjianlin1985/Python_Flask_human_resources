import re

from flask import current_app, jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import session

from person import db
from person.models import User,Department

from person.utils.response_code import RET
from . import Admin

# 添加员工数据
@Admin.route("/add_admindepartment", methods=['POST'])
def add_admindepartment():
    # 获取参数
    auser_id = request.json.get('auser_id')
    auser_name = request.json.get('auser_name')
    auser_age = request.json.get('auser_age')
    auser_gender = request.json.get('auser_gender')
    auser_department = request.json.get('auser_department')
    auser_tel = request.json.get('auser_tel')
    auser_email = request.json.get('auser_email')
    # 检查参数的完整性
    if not all([ auser_id,auser_name,auser_age,auser_gender,auser_department,auser_tel,auser_email]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')
    # 校验是否int类型
    try:
        auser_id = int(auser_id)
        auser_age = int(auser_age)
        auser_department = int(auser_department)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数类型错误')
    # 检查性别
    if auser_gender not in ['MAN', 'WOMAN']:
        return jsonify(errno=RET.PARAMERR, errmsg='性别参数错误')
    # 检查手机号
    if not re.match(r'1[3456789]\d{9}$', auser_tel):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号格式错误')
    # 检查邮箱格式
    if not re.match(r'[0-9a-z][_.0-9a-z-]{0,31}@([0-9a-z][0-9a-z-]{0,30}[0-9a-z]\.){1,4}[a-z]{2,4}$', auser_email):
        return jsonify(errno=RET.PARAMERR, errmsg='邮箱格式错误')
    # 从数据库获取数据
    try:
        user = User.query.filter_by(user_id=auser_id).first()

        if user.is_deleted == 1:
            user.is_deleted = 0
            user.user_id = auser_id
            user.user_name = auser_name
            user.user_age = auser_age
            user.user_gender = auser_gender
            user.user_mobile = auser_tel
            user.user_email = auser_email
            user.depart_id = auser_department
        else:
            return jsonify(errno=RET.DATAERR, errmsg='用户已存在')
    except Exception as e:
        # 构建模型类对象
        user = User()
        user.user_id = auser_id
        user.user_name = auser_name
        user.user_age = auser_age
        user.user_gender = auser_gender
        user.user_mobile = auser_tel
        user.user_email = auser_email
        user.depart_id = auser_department
    # 存入数据库
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存数据失败')
        # 返回前端数据
    return jsonify(errno='0', errmsg='OK')
# 编辑员工数据
@Admin.route("/editor_admindepartment", methods=['PUT'])
def editor_admindepartment():
    # 获取参数
    userId = request.json.get('userId')
    euser_id = request.json.get('euser_id')
    euser_name = request.json.get('euser_name')
    euser_age = request.json.get('euser_age')
    euser_gender = request.json.get('euser_gender')
    euser_department = request.json.get('euser_department')
    euser_tel = request.json.get('euser_tel')
    euser_email = request.json.get('euser_email')
    # 检查参数的完整性
    if not all([userId, euser_id,euser_name, euser_age,euser_gender,euser_department,euser_tel,euser_email]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')
    # 校验是否int类型
    try:
        userId = int(userId)
        euser_id = int(euser_id)
        euser_age = int(euser_age)
        euser_department = int(euser_department)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数类型错误')
    # 检查性别
    if euser_gender not in ['MAN', 'WOMAN']:
        return jsonify(errno=RET.PARAMERR, errmsg='性别参数错误')
    # 检查手机号
    if not re.match(r'1[3456789]\d{9}$', euser_tel):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号格式错误')
    # 检查邮箱格式
    if not re.match(r'[0-9a-z][_.0-9a-z-]{0,31}@([0-9a-z][0-9a-z-]{0,30}[0-9a-z]\.){1,4}[a-z]{2,4}$', euser_email):
        return jsonify(errno=RET.PARAMERR, errmsg='邮箱格式错误')
    # 检查要编辑的对象和输入的是否一致
    if userId!=euser_id:
        return jsonify(errno=RET.DATAERR, errmsg='要删除的员工和输入的不一致错误')
    # 构建模型类对象
    try:
        user = User.query.filter_by(user_id=userId).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询员工错误')
    if user.is_deleted == 0:
        user.user_name = euser_name
        user.user_age = euser_age
        user.user_gender = euser_gender
        user.user_mobile = euser_tel
        user.user_email = euser_email
        user.depart_id = euser_department
    else:
        return jsonify(errno=RET.DBERR, errmsg='员工被逻辑删除')
    # 存入数据库
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存数据失败')
        # 返回前端数据
    return jsonify(errno=RET.OK, errmsg='OK')
# 删除员工
@Admin.route("/delete_user", methods=['DELETE'])
def delete_user():
    # 获取参数
    userId = request.json.get('userId')
    # 检查参数的完整性
    if not all([userId]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')
    # 校验是否int类型
    try:
        userId = int(userId)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数类型错误')

    # 查询数据
    try:
        user = User.query.filter_by(user_id=userId).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询员工数据错误')
    user.is_deleted = 1
    # 存入数据库
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='删除员工数据失败')
        # 返回前端数据
    return jsonify(errno='0', errmsg='OK')
# 管理员退出
@Admin.route("/exit_admin", methods=['POST'])
def exit_admin():
    print(session)
    session.pop('admin_id', None)
    session.pop('admin_psw', None)
    print(session)
    return jsonify(errno='0', errmsg='OK')


# 管理员界面
@Admin.route("/Admin.html")
def Admin():
    try:
        # 获取用户状态保持信息
        superadmin_id = session['admin_id']
        superadmin_psw = session['admin_psw']
    except Exception as e:
        current_app.logger.error(e)
        return redirect('/')

    # 从数据库获取用户数据
    try:
        users = User.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询管理员数据失败')
    # 判断查询结果
    if not users:
        return jsonify(errno=RET.NODATA, errmsg='无管理员数据')
    # 从数据库获取用户数据
    try:
        departments = Department.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询部门数据失败')
    # 判断查询结果
    if not departments:
        return jsonify(errno=RET.NODATA, errmsg='无部门数据')
    # 定义列表，存储部门数据
    department_list = []
    for department in departments:
        department_list.append(department)
    # 定义列表，存储用户数据
    users_list = []
    for user in users:
        users_list.append(user.to_dict())
    # 定义列表，存储数据
    data = {
        'users': users_list,
        'departments':department_list
    }
    return render_template('Admin.html', data=data)
