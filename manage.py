#!/usr/bin/env python3
from app import create_app, config
from app.data import db
from flask_migrate import Migrate, MigrateCommand
from flask_script import (
    Server,
    Shell,
    Manager,
)

def _make_context():
    return dict(
        app=create_app(config.dev_config),
        db=db,
    )

app = create_app(config=config.dev_config)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('runserver', Server(host='0.0.0.0'))
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
