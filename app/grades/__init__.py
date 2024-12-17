from flask import Flask
from flask import Blueprint

grades_bp = Blueprint("grades", __name__, url_prefix="/grades", template_folder="templates", static_folder="static", static_url_path="static")

from . import views