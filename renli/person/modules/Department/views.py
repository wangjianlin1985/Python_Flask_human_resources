from flask import current_app
from flask import redirect
from flask import render_template, jsonify
from flask import request
from flask import session

from person import db
from person.models import Department
from person.utils.response_code import RET
from . import Departments


# 添加部门数据
@Departments.route("/add_department", methods=['POST'])
def add_department():
    # 获取参数
    department_id = request.json.get('department_id')
    department_name = request.json.get('department_name')
    # 检查参数的完整性
    if not all([department_id, department_name]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')
    # 校验是否int类型
    try:
        department_id = int(department_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数类型错误')

    # 新增
    # 从数据库获取数据
    try:
        departments = Department.query.filter_by(depart_id=department_id).first()
        if departments.is_deleted == 1:
            departments.is_deleted = 0
            departments.depart_name = department_name
        else:
            return jsonify(errno=RET.DATAERR, errmsg='已存在')
    except Exception as e:
        # 构建模型类对象
        departments = Department()
        departments.depart_id = department_id
        departments.depart_name = department_name
    # 存入数据库
    try:
        db.session.add(departments)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存数据失败')
        # 返回前端数据
    return jsonify(errno='0', errmsg='OK')

# 添加和编辑部门数据
@Departments.route("/edit_department", methods=['PUT'])
def edit_department():
    # 获取参数
    department_id_ = request.json.get('department_id_')
    department_id = request.json.get('department_id')
    department_name = request.json.get('department_name')
    # 检查参数的完整性
    if not all([department_id, department_name,department_id_]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')
    # 校验是否int类型
    try:
        department_id = int(department_id)
        department_id_ = int(department_id_)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数类型错误')

    if department_id!=department_id_:
        return jsonify(errno=RET.PARAMERR, errmsg='参数类型错误')
    # 新增
    # 从数据库获取数据
    try:
        department = Department.query.filter_by(depart_id=department_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询部门数据错误')
    department .depart_id = department_id
    department.depart_name = department_name
    # 存入数据库
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存数据失败')
        # 返回前端数据
    return jsonify(errno='0', errmsg='OK')

# 删除部门数据
@Departments.route("/delete_department", methods=['DELETE'])
def delete_department():
    # 获取参数
    department_id = request.json.get('department_id')
    department_name = request.json.get('department_name')
    # 检查参数的完整性
    if not all([department_id, department_name]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')
    # 校验是否int类型
    try:
        department_id = int(department_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg='参数类型错误')

    # 构建模型类对象
    try:
        department = Department.query.filter_by(depart_id=department_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询部门数据错误')
    department.is_deleted = 1
    # 存入数据库
    try:
        db.session.add(department)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='删除部门数据失败')
        # 返回前端数据
    return jsonify(errno='0', errmsg='OK')


# 退出登录
@Departments.route("/exit_department", methods=['POST'])
def exit_department():
    session.pop('admin_id', None)
    session.pop('admin_psw', None)
    print(session)
    return jsonify(errno='0', errmsg='OK')


# 部门界面
@Departments.route("/Department.html")
def Departments():
    try:
        # 获取用户状态保持信息
        superadmin_id = session['admin_id']
        superadmin_psw = session['admin_psw']
    except Exception as e:
        current_app.logger.error(e)
        return redirect('/')

    # 从数据库获取数据
    try:
        departments = Department.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询管理员数据失败')
    # 判断查询结果
    if not departments:
        return jsonify(errno=RET.NODATA, errmsg='无管理员数据')
    # 定义列表，存储数据
    data = {
        'departments': departments
    }
    return render_template('Department.html', data=data)
