from flask import render_template
from flask import Blueprint, session
import info

index_blue = Blueprint('index', __name__, static_folder='../../static', template_folder='../../templates/news')


@index_blue.route('/')
def index():
    redis_store = info.create_app()[2]
    session['name'] = 'yh'
    redis_store.set('gender', 'male')
    return render_template('index.html')
