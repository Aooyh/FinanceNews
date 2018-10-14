from flask import current_app
from flask import render_template
from flask import Blueprint, session
from info.utils.captcha.captcha import captcha
import info

index_blue = Blueprint('index', __name__, static_folder='../../static/news', template_folder='../../templates/news')


@index_blue.route('/')
def index():
    redis_store = info.create_app()[2]
    session['name'] = 'yh'
    redis_store.set('gender', 'male')
    return render_template('index.html')


@index_blue.route('/favicon.ico')
def send_ico():
    return current_app.send_static_file('favicon.ico')


@index_blue.route('/image_code')
def image_code():
    image_data = captcha.generate_captcha()[2]
    return image_data
