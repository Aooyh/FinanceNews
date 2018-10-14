from info import create_app
from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate


app, db, redis_store = create_app('product')
manager = Manager(app)
Migrate(app, db)
manager.add_command('dbc', MigrateCommand)


if __name__ == '__main__':
    manager.run()
