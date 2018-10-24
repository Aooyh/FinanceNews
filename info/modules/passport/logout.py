from flask import session, jsonify, request, render_template
from info.response_code import *

def logout():
    """
    通过退出按钮请求
    :return:
    """
    session.pop('user_id', None)
    session.pop('is_admin', None)
    if request.json:
        render_template('news/index.html')
    else:
        return jsonify(errno=RET.OK, errmsg='退出成功')
