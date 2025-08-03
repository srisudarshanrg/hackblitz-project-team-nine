from flask import Blueprint, render_template, request, flash, url_for, redirect
from .models import Buyer, Seller
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user
from . import session

auth = Blueprint("auth", __name__)


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get("role")

        if role == "Buyer":
            query_table = Buyer
        if role == "Seller":
            query_table = Seller
        
        if user := query_table.query.filter_by(username=username).first():
            if check_password_hash(user.password, password):
                login_user(user)
                session["user_type"] = role.lower()
                return redirect(url_for('home.homepage'))
            else:
                flash("Incorrect password. Try again!", category="danger")
        else:
            flash("User does not exist", category="danger")
    return render_template("login.html")

@auth.route('/signup/', methods=['GET', 'POST'])
def sign_up():
    from . import db    
    
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        role = request.form.get("role")

        print(role)

        print(password1)
        print(password2)

        if role == "Buyer":
            query_table = Buyer
        else:
            query_table = Seller
        
        if user := query_table.query.filter_by(username=username).first():
            flash("Username already exists.", category="danger")
        elif len(username) < 4:
            flash("Email must be greater than 4 characters.", category="danger")
        elif password1 != password2:
            flash("Passwords don\'t match.", category="danger")
        elif len(password1) < 7:
            flash("Password must be at least 7 characters.", category="danger")
        else:
            new_user = query_table(username=username, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            session["user_type"] = role.lower()
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