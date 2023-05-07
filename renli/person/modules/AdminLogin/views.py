from . import AdminLogin
from flask import current_app
from flask import render_template, jsonify
from flask import request
from flask import session, redirect

from person.models import Admin
from person.utils.response_code import RET


# 超级管理员登录界面

@AdminLogin.route("/adminlogin", methods=['POST'])
def login():
    # 获取参数
    admin_id = request.json.get('admin_id')
    admin_psw = request.json.get('admin_psw')
    try:
        admin = Admin.query.filter_by(admin_id=admin_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg='查询用户账号失败')
    try:
        admin_psw = Admin.query.filter_by(admin_psw=admin_psw).first().admin_psw
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg='查询用户密码失败')

    if admin.admin_psw != admin_psw:
        return jsonify(errno=RET.PWDERR, errmsg='用户名和密码不匹配')
    if not admin or not admin_psw:
        return jsonify(errno=RET.PWDERR, errmsg='用户名或密码错误')
    # 实现状态保持
    try:
        session['admin_id'] = admin.admin_id
        session['admin_psw'] = admin.admin_psw
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='实现状态保持失败')
    return jsonify(errno=RET.OK, errmsg='OK')


@AdminLogin.route("/AdminLogin.html")
def AdminLogin():
    try:
        # 获取用户状态保持信息
        superadmin_id = session['admin_id']
        superadmin_psw = session['admin_psw']
    except Exception as e:
        current_app.logger.error(e)
        return render_template('AdminLogin.html')
    return redirect('/AdminChoose.html')
