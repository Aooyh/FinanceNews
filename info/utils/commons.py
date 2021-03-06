from flask import g, current_app, session, jsonify
from info.response_code import *
from functools import wraps


def news_filter(index):
    if index == 1:
        return 'first'
    elif index == 2:
        return 'second'
    elif index == 3:
        return 'third'
    else:
        return ''


def log_in_ifo(view_fun):
    @wraps(view_fun)
    def wrapper(*args, **kwargs):
        try:
            user_id = session.get('user_id')
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])
        if user_id:
            from info.models import User
            g.user = User.query.get(int(user_id))
            g.user_info = g.user.to_dict()
        else:
            g.user = ''
            g.user_info = ''
        return view_fun(*args, **kwargs)
    return wrapper
