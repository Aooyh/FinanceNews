from flask_migrate import MigrateCommand, Migrate
from info.modules.index import index_blue
from info.modules.user_info.views import *
from info.modules.passport.views import *
from info.modules.detail.views import *
from info.modules.admin.views import *
from flask_script import Manager
from info.models import app, db

app.register_blueprint(index_blue)
app.register_blueprint(passport_blue)
app.register_blueprint(detail_blue)
app.register_blueprint(user_info_blue)
app.register_blueprint(admin_blue)
manager = Manager(app)
Migrate(app, db)
print(app.url_map)
manager.add_command('dbc', MigrateCommand)


@manager.option('-p', '--password', dest='password')
@manager.option('-u', '--username', dest='username')
def create_admin(username, password):
    admin = User()
    admin.mobile = username
    admin.nick_name = username
    admin.password = password
    admin.is_admin = True
    try:
        db.session.add(admin)
        db.session.commit()
        return '创建成功'
    except Exception as e:
        current_app.logger(e)
        return '创建失败'


if __name__ == '__main__':
    manager.run()
