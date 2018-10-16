from flask_script import Manager
from info.modules.index import index_blue
from info.modules.passport.views import *
from flask_migrate import MigrateCommand, Migrate
from info.models import *

app, db, redis_store = create_app('testing')
app.register_blueprint(index_blue)
app.register_blueprint(passport_blue)
manager = Manager(app)
Migrate(app, db)
manager.add_command('dbc', MigrateCommand)


if __name__ == '__main__':
    manager.run()
