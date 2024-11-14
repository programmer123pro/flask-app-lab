from flask import request, redirect, url_for, render_template, abort
from . import app

@app.route("/")
def main():
    return "Hello world!"

@app.route('/homepage') 
def home():
    """View for the Home page of your website."""
    agent = request.user_agent

    return render_template("home.html", agent=agent)

#users

@app.route("/hi/<string:name>")   #/hi/ivan?age=45
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)            

    return render_template("hi.html",
                           name=name, age=age)