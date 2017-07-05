import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt


# instantiate the db
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app():
    # instantiate the app
    app = Flask(__name__)

    # 解决跨域请求的问题
    CORS(app)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # setup extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from plato.api.users import users_blueprint
    from plato.api.auth import auth_blueprint
    app.register_blueprint(users_blueprint)
    app.register_blueprint(auth_blueprint)

    return app
