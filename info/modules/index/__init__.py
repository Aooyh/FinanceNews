from flask import current_app, session, jsonify
from flask import render_template
from info.response_code import *
from info.models import User
from flask import Blueprint

index_blue = Blueprint('index', __name__, template_folder='../../templates/news')


@index_blue.route('/')
def index():
    try:
        user_id = session.get('user_id')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg=error_map[RET.DBERR])
    if user_id:
        user_info = User.query.get(user_id).to_dict()
    else:
        user_info = ''
    return render_template('index.html', user_info=user_info)


@index_blue.route('/favicon.ico')
def send_ico():
    return current_app.send_static_file('news/favicon.ico')
