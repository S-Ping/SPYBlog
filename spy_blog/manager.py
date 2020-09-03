__author__ = 'SPing'

import os
from flask_script import Manager
from dotenv import load_dotenv, find_dotenv
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db

load_dotenv('.env', verbose=True)
app = create_app(os.environ.get('FLASK_ENV', 'development'))
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
