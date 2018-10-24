from flask import render_template, request, redirect, current_app, jsonify, session, g
from info.response_code import *
from info.utils.commons import log_in_ifo
from info.models import User

def login():
    """
    管理员账户登录
    :return:
    """
    if request.method == 'GET':
        if session.get('is_admin'):
            return redirect('admin/index')
        return render_template('login.html')
    username = request.form.get('username')
    password = request.form.get('password')
    try:
        user = User.query.filter(User.mobile == username).first()
        if user:
            if not user.is_admin:
                return render_template('login.html', errmsg='该用户不是管理员')
            if user.check_passowrd(password):
                session['user_id'] = user.id
                session['is_admin'] = True
                return redirect('/admin/index')
            else:
                return render_template('login.html', errmsg='密码不正确')
        else:
            return render_template('login.html', errmsg='不存在此用户')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])

@log_in_ifo
def index():
    """
    后台管理首页界面
    :return:
    """
    return render_template('admin/index.html', user_info=g.user_info)
