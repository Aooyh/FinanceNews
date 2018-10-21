from flask import Blueprint

user_info_blue = Blueprint('user_info', __name__, template_folder='../../templates/user', url_prefix='/user_info')
