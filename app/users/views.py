from flask import *
from . import users_bp

@users_bp.route('/')
def home():
    myName = "Іванків Тарас"
    return render_template('hi.html', name=myName)

@users_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)            

    return render_template("hi.html", name=name, age=age)

@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)     # "http://localhost:8080/hi/administrator?age=45"
    print(to_url)
    return redirect(to_url)

users = {
    'taras' : "123"
}

@users_bp.route("/login", methods=['GET', 'POST'])
def login():
    if(request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')
 
        if(username and password):
            if(username in users and users[username] == password):
                session['username'] = username
                flash('Login successfull', 'success')
                return redirect(url_for('users.profile'))
            else:   
               flash('Login failed. Please try again.', 'danger') 
    
    return render_template("login.html")

@users_bp.route("/profile")
def profile():
    if('username' in session):
        cookies = list(request.cookies.items())
        dark_theme = False 
        if ('theme' in request.cookies) and (request.cookies['theme'] == 'dark'):
            dark_theme = True
        return render_template("profile.html", username=session['username'], cookies=cookies, dark_theme=dark_theme)
    else:
        return redirect(url_for('users.login'))

@users_bp.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('users.login')) 

@users_bp.route('/cookies', methods=['POST'])
def cookies():
    response = redirect(url_for('users.profile'))
    method = request.form.get('_method')

    if method == 'POST':
        cookieKey = request.form.get('cookieKey')
        cookieValue = request.form.get('cookieValue')
        term = int(request.form.get('cookieExpires')) * 86400
        response.set_cookie(cookieKey, cookieValue, term)
        flash('Cookie успішно додано!', 'success')
    
    elif method == 'DELETE':
        cookieKey = request.form.get('deleteKey')
        if cookieKey in request.cookies:
            response.delete_cookie(cookieKey)
            flash('Cookie успішно видалено!', 'success')
        else:
            flash('Такого Cookie не знайдено!', 'error')

    elif method == 'ALL_DELETE':
            for cookie in request.cookies:
                response.delete_cookie(cookie)
            flash('Cookies успішно видалені!', 'success')
            
    return response

@users_bp.route('/change_theme')
def theme():
    response = redirect(url_for('users.profile')) 
    if not('theme' in request.cookies) or (request.cookies['theme'] == 'light'):
        response.set_cookie('theme', 'dark')
    elif(request.cookies['theme'] == 'dark'):
        response.set_cookie('theme', 'light')
    return response
        

            