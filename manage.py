#!/usr/bin/env python3
from app import create_app, config
from app.data import db
from flask_migrate import Migrate

app = create_app(config=config.dev_config)

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()
