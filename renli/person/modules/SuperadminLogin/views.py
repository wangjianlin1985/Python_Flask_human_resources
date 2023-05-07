import re

from flask import current_app
from flask import render_template, jsonify
from flask import request
from flask import session, redirect, url_for

from person.models import SuperAdmin
from person.utils.response_code import RET
from . import SuperadminLogin
from person.modules.Superson.views import Supersons


@SuperadminLogin.route("/superadminlogin", methods=['POST'])
def login():
    # 获取参数
    superadmin_id = request.json.get('superadmin_id')
    superadmin_password = request.json.get('superadmin_password')
    try:
        superadmin = SuperAdmin.query.filter_by(superadmin_id=superadmin_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg='查询用户账号失败')
    try:
        superadmin_psw = SuperAdmin.query.filter_by(superadmin_psw=superadmin_password).first().superadmin_psw
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg='查询用户密码失败')
    print(superadmin_psw)
    if superadmin.superadmin_psw != superadmin_psw:
        return jsonify(errno=RET.PWDERR, errmsg='用户名和密码不匹配')
    if not superadmin or not superadmin_psw:
        return jsonify(errno=RET.PWDERR, errmsg='用户名或密码错误')
    # 实现状态保持
    try:
        session['superadmin_id'] = superadmin.superadmin_id
        session['superadmin_psw'] = superadmin.superadmin_psw
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='实现状态保持失败')
    return jsonify(errno=RET.OK, errmsg='OK')


# 超级管理员登录界面
@SuperadminLogin.route("/SuperadminLogin.html")
def SuperadminLogin():
    try:
        # 获取用户状态保持信息
        superadmin_id = session['superadmin_id']
        superadmin_psw = session['superadmin_psw']
    except Exception as e:
        current_app.logger.error(e)
        return render_template('SuperadminLogin.html')
    return redirect('/Superson.html')