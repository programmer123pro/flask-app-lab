from flask import Blueprint

resume_bp = Blueprint("resume", __name__, url_prefix="/resume", template_folder="templates",
                    static_url_path="static/", static_folder="static/")

from . import views 