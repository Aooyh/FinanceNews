from flask_migrate import MigrateCommand, Migrate
from info.modules.index import index_blue
from info.modules.user_info.views import *
from info.modules.passport.views import *
from info.modules.detail.views import *
from flask_script import Manager
from info.models import app, db

app.register_blueprint(index_blue)
app.register_blueprint(passport_blue)
app.register_blueprint(detail_blue)
app.register_blueprint(user_info_blue)
manager = Manager(app)
Migrate(app, db)
print(app.url_map)
manager.add_command('dbc', MigrateCommand)


if __name__ == '__main__':
    manager.run()
