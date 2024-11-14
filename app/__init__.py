from flask import Flask

app = Flask(__name__, template_folder="templates")
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config.from_pyfile("../config.py")
from . import views

from .resume import resume_bp
app.register_blueprint(resume_bp)

from .users import users_bp
app.register_blueprint(users_bp)

from .posts import posts_bp
app.register_blueprint(posts_bp)
