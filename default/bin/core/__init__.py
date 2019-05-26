from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
import jinja2
from flask import Flask
from core.config import Config, app_path
from core.utils.app_utils import get_theme
from mods.config import static_path, templates_path
from werkzeug.contrib.fixers import ProxyFix


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__, static_folder=app_path + static_path)

    app.wsgi_app = ProxyFix(app.wsgi_app) # Magic fix from the interweb. -
    # https://stackoverflow.com/questions/34802316/make-flasks-url-for-use-the-https-scheme-in-an-aws-load-balancer-without-mess
    # http://werkzeug.pocoo.org/docs/0.12/contrib/fixers/#werkzeug.contrib.fixers.ProxyFix

    app.config.from_object(config_class)

    db.init_app(app)

    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Creating new template loader
    my_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader(app_path + templates_path),
    ])
    app.jinja_loader = my_loader

    # Core app routes
    from core.routes.routes import default
    app.register_blueprint(default)

    from core.users.routes import users
    app.register_blueprint(users)

    # Add on application routes
    from mods.app_api.routes.routes import app_default
    app.register_blueprint(app_default)

    # Add on application routes
    from mods.app_ui.main.routes import main
    app.register_blueprint(main)

    # create db from models
    app.app_context().push()
    db.create_all()

    app.jinja_env.globals.update(get_theme=get_theme)

    return app
