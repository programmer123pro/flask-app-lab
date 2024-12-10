from flask import *
from . import users_bp
from .forms import *
from app import bcrypt, login_manager
from flask_login import *

@users_bp.route('/')
def home():
    myName = "Іванків Тарас"
    return render_template('hi.html', name=myName, logined = current_user.is_authenticated)

@users_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)            

    return render_template("hi.html", name=name, age=age, logined = current_user.is_authenticated)

@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)     # "http://localhost:8080/hi/administrator?age=45"
    print(to_url)
    return redirect(to_url)


@users_bp.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if(request.method == 'GET'):
        return render_template("login.html", form=form, logined = current_user.is_authenticated)
    
    elif(request.method == 'POST'):
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            user = User.query.filter(User.username == username).first()
            if user and user.check_password(password):
                login_user(user)
                flash('Login successfull', 'success')
                return redirect(url_for('users.profile'))
            else:   
               flash('Login failed. Please try again.', 'danger')
               return redirect(url_for('.login'))
        return render_template('login.html', form=form, logined = current_user.is_authenticated)

@users_bp.route("/profile") 
@login_required
def profile():
    cookies = list(request.cookies.items())
    dark_theme = False 
    if ('theme' in request.cookies) and (request.cookies['theme'] == 'dark'):
        dark_theme = True
    return render_template("profile.html", user=current_user, cookies=cookies, dark_theme=dark_theme, logined = current_user.is_authenticated)

@users_bp.route('/logout')
def logout():
    logout_user()
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

@users_bp.route('/sign_up/', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if(request.method == 'GET'):
        return render_template("sign_up.html", form=form, logined = current_user.is_authenticated)
    
    elif(request.method == 'POST'):
        if form.validate_on_submit():
            user = User(
                username = form.username.data,
                email = form.email.data,
                password = form.password.data
                )
            user.hash_password()
            db.session.add(user)
            db.session.commit()
            flash('User signed up successful', 'success')
            return redirect(url_for('.sign_up'))
        return render_template('sign_up.html', form=form, logined = current_user.is_authenticated)


@users_bp.route('/all_users/')
@login_required
def show_all_users():
    users = User.query.all()
    if len(users) > 0:
        return render_template("all_users.html", users=users, logined = current_user.is_authenticated)
    else: 
        return render_template("all_users.html", users=None, logined = current_user.is_authenticated)
        

            
        

            