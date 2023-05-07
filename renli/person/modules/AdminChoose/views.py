from . import AdminChoose
from flask import current_app
from flask import render_template
from flask import session

@AdminChoose.route("/AdminChoose.html")
def AdminChoose():
    try:
        # 获取用户状态保持信息
        superadmin_id = session['admin_id']
        superadmin_psw = session['admin_psw']
    except Exception as e:
        current_app.logger.error(e)
        return render_template('AdminLogin.html')
    return render_template('AdminChoose.html')