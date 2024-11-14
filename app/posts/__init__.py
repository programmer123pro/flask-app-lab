from flask import Flask
from flask import Blueprint

posts_bp = Blueprint('posts', __name__, url_prefix='/posts', template_folder='templates/posts',
                    static_url_path="static/", static_folder="static/")

from . import views