from . import resume_bp
from flask import *

@resume_bp.route('/')
def resume():
    myName = "Іванків Тарас"
    return render_template('resume/resume.html', name=myName)
