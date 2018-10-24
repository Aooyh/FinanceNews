from flask import session, jsonify, current_app
from info.response_code import *
from datetime import datetime
from info.models import User
from flask import request


def login():
    """
    用户登录请求
    点击登录表单的登录按钮时
    通过submit方法的ajax请求执行
    :return:
    """
    login_info = request.json
    mobile = login_info.get('mobile')
    password = login_info.get('password')
    try:
        user = User.query.filter(User.mobile == mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])
    if user:
        if user.check_passowrd(password):
            try:
                session['user_id'] = user.id
                session['is_admin'] = user.is_admin
                user.last_login = datetime.now()
            except Exception as e:
                current_app.logger.error(e)
                return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])
            return jsonify(errno=RET.OK, errmsg='登录成功')
        else:
            return jsonify(errno=RET.DATAERR, errmsg='密码与账户不匹配!')
    else:
        return jsonify(errno=RET.DATAERR, errmsg='不存在此账户')
