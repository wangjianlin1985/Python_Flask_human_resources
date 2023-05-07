import re

from flask import current_app
from flask import redirect
from flask import render_template, jsonify
from flask import request
from flask import session

from person import db
from person.models import Recruiter, User
from person.utils.response_code import RET
from . import Resource

# 添加员工数据
@Resource.route("/add_newusersfrom", methods=['POST'])
def add_newusersfrom():
    # 获取参数
    auser_id = request.json.get('auser_id')
    auser_name = request.json.get('auser_name')
    auser_age = request.json.get('auser_age')
    auser_gender = request.json.get('auser_gender')
    auser_tel = request.json.get('auser_tel')
    auser_email = request.json.get('auser_email')
    # 检查参数的完整性
    if not all([ auser_id,auser_name,auser_age,auser_gender,auser_tel,auser_email]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')
    # 校验是否int类型
    try:
        auser_id = int(auser_id)
        auser_age = int(auser_age)
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
    # 构建模型类对象
    recruiter = Recruiter()
    recruiter.recruiter_id = auser_id
    recruiter.recruiter_name = auser_name
    recruiter.recruiter_age = auser_age
    recruiter.recruiter_gender = auser_gender
    recruiter.recruiter_mobile = auser_tel
    recruiter.recruiter_email = auser_email
    # 存入数据库
    try:
        db.session.add(recruiter)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存数据失败')
        # 返回前端数据
    return jsonify(errno='0', errmsg='OK')



# 编辑员工数据
@Resource.route("/edi_newusersfrom", methods=['PUT'])
def edi_newusersfrom():
    # 获取参数
    userId = request.json.get('userId')
    euser_id = request.json.get('euser_id')
    euser_name = request.json.get('euser_name')
    euser_age = request.json.get('euser_age')
    euser_gender = request.json.get('euser_gender')
    euser_tel = request.json.get('euser_tel')
    euser_email = request.json.get('euser_email')
    # 检查参数的完整性
    if not all([userId, euser_id,euser_name, euser_age,euser_gender,euser_tel,euser_email]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数缺失')
    # 校验是否int类型
    try:
        userId = int(userId)
        euser_id = int(euser_id)
        euser_age = int(euser_age)
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
        return jsonify(errno=RET.DATAERR, errmsg='要删除的招聘人员和输入的不一致错误')
    # 构建模型类对象
    try:
        recruiter = Recruiter.query.filter_by(recruiter_id=euser_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询员工错误')
    recruiter.recruiter_id = euser_id
    recruiter.recruiter_name = euser_name
    recruiter.recruiter_age = euser_age
    recruiter.recruiter_gender = euser_gender
    recruiter.recruiter_mobile = euser_tel
    recruiter.recruiter_email = euser_email
    # 存入数据库
    try:
        db.session.add(recruiter)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='保存数据失败')
        # 返回前端数据
    return jsonify(errno=RET.OK, errmsg='OK')

# 删除员工
@Resource.route("/delete_newuser", methods=['DELETE'])
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

    # 构建模型类对象
    try:
        recruiter = Recruiter.query.filter_by(recruiter_id=userId).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询招聘人员数据错误')

    # 存入数据库
    try:
        db.session.delete(recruiter)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='删除招聘人员数据失败')
        # 返回前端数据
    return jsonify(errno='0', errmsg='OK')

# 退出登录
@Resource.route("/exit_resource", methods=['POST'])
def exit_resource():
    session.pop('admin_id', None)
    session.pop('admin_psw', None)
    return jsonify(errno='0', errmsg='OK')
# 招聘界面
@Resource.route("/Resource.html")
def Resource():
    try:
        # 获取用户状态保持信息
        superadmin_id = session['admin_id']
        superadmin_psw = session['admin_psw']
    except Exception as e:
        current_app.logger.error(e)
        return redirect('/')

    # 从数据库获取数据
    try:
        Recruiters = Recruiter.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询管理员数据失败')
    # 判断查询结果
    if not Recruiters:
        return jsonify(errno=RET.NODATA, errmsg='无管理员数据')
    # 定义列表，存储数据
    data = {
        'Recruiters': Recruiters
    }
    return render_template('Resource.html', data=data)
