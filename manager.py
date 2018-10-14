from flask_script import Manager
from info.modules.index import index_blue
from flask_migrate import MigrateCommand, Migrate
from info.models import *


app = create_app('testing')[0]
app.register_blueprint(index_blue)
manager = Manager(app)
Migrate(app, db)
manager.add_command('dbc', MigrateCommand)


if __name__ == '__main__':
    manager.run()
