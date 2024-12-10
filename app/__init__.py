from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

class Base(DeclarativeBase):
    pass    

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app(config_name='config.DevConfig'):

    app = Flask(__name__, template_folder="templates")
    app.config.from_object(config_name)

    from .posts.models import Post
    from .users.models import User
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    login_manager.login_view = 'users.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    with app.app_context():
        from . import views
    
        from .resume import resume_bp
        app.register_blueprint(resume_bp)

        from .users import users_bp
        app.register_blueprint(users_bp)

        from .posts import posts_bp
        app.register_blueprint(posts_bp)
    
    return app