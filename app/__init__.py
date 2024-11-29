from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass    

db = SQLAlchemy(model_class=Base)
migrate = Migrate()

def create_app(config_name='config'):

    app = Flask(__name__, template_folder="templates")
    app.config.from_object(config_name)

    from .posts.models import Post
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from . import views
    
        from .resume import resume_bp
        app.register_blueprint(resume_bp)

        from .users import users_bp
        app.register_blueprint(users_bp)

        from .posts import posts_bp
        app.register_blueprint(posts_bp)
    
    return app