from flask import Blueprint, render_template, request, flash, url_for, redirect
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user

auth = Blueprint("auth", __name__)


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if user := User.query.filter_by(email=email).first(): # := is assignment with check
            print('here')
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('home.homepage'))
            else:
                flash("Incorrect password. Try again!", category="error")
        else:
            flash("Email does not exist", category="error")
    return render_template("login.html")

@auth.route('/signup/', methods=['GET', 'POST'])
def sign_up():
    from . import db    
    
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstname')
        password1 = request.form.get('psw')
        password2 = request.form.get('psw-repeat')
        print('here')
        
        if user := User.query.filter_by(email=email).first():
            flash("Email already exists.", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 4 characters.", category="error")
        elif len(first_name) < 2:
            flash("First name must be greater than 1 character.", category="error")
        elif password1 != password2:
            flash("Passwords don\'t match.", category="error")
        elif len(password1) < 7:
            flash("Password must be at least 7 characters.", category="error")
        else:
            new_user = User(email=email, firstname=first_name, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('home.homepage'))
    return render_template("sign_up.html")

@auth.route('/forgot_pwd/')
def forgot_pwd():
    return render_template("forgot_pwd.html")

@auth.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))