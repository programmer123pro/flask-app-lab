from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route("/")
def main():
    return "Hello world!"

@app.route("/resume")
def resume():
    myName = "Іванків Тарас"
    return render_template('resume.html', name=myName)

if __name__ == "__main__":
    app.run(debug=True) 