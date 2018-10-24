from flask import Blueprint, session, redirect, request

admin_blue = Blueprint('admin', __name__, url_prefix='/admin', template_folder='../../templates/admin')


@admin_blue.before_request
def admin_visit():
    if not session.get('is_admin'):
        if not request.url.endswith('login'):
            return redirect('/')
