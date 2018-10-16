from flask import session, jsonify
from info.response_code import *

def logout():
    """
    通过退出按钮请求
    :return:
    """
    session.pop('user_id')
    return jsonify(errno=RET.OK, errmsg='退出成功')
