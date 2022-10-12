from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

migrate = Migrate()
bcrypt = Bcrypt()
lm = LoginManager()
