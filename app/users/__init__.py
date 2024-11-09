from flask import Blueprint

users_bp = Blueprint("users", __name__, url_prefix="/users", template_folder="templates/users",
                       static_url_path="static/", static_folder="static/")


from . import views

