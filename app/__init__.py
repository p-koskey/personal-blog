from flask import Flask
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
from config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_uploads import UploadSet,configure_uploads,IMAGES

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

db =  SQLAlchemy()
fa = FontAwesome()
bootstrap = Bootstrap()
photos = UploadSet('photos',IMAGES)
mail = Mail()
def create_app(config_name):

    app = Flask(__name__)

    #create app configurations
    from flask_bootstrap import Bootstrap
    app.config.from_object(config_options[config_name])
    config_options[config_name].init_app(app)

    # Initializing flask extensions
    bootstrap.init_app(app)
    fa.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

     # Registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix = '/authenticate')

    # configure UploadSet
    configure_uploads(app,photos)

     # setting config
    from .requests import configure_request
    configure_request(app)

    return app