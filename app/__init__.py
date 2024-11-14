from flask import Flask

def create_app(config_name='../config.py'):

    app = Flask(__name__, template_folder="templates")
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config.from_pyfile(config_name)

    with app.app_context():
        from . import views

        from .resume import resume_bp
        app.register_blueprint(resume_bp)

        from .users import users_bp
        app.register_blueprint(users_bp)

        from .posts import posts_bp
        app.register_blueprint(posts_bp)
    
    return app