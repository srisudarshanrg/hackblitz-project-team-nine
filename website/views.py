import ollama
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from .functions import roles_required
from . import session

home = Blueprint("home", __name__)

client = ollama.Client()
model = "llama3.2"

@home.route("/")
def homepage():
    print(current_user)
    return render_template("homepage.html", user=current_user, role=current_user.get_role())

@home.route("/seller-marketplace", methods=["GET", "POST"])
@roles_required("seller")
@login_required
def seller_marketplace():
    if request.method == "POST":
        if "price_predictor" in request.form:
            crop_name = request.form.get("crop_name")
            quantity = request.form.get("quantity")
            state = request.form.get("state")
            weather = request.form.get("weather")

            prompt = (
                f"You are an API. Only return a number. For example:\n"
                f"Input: wheat, 100 quintals, sunny, Punjab\n give price prediction"
                f"Output: 85000\n\n"
                f"Now:\n"
                f"Input: {crop_name}, {quantity} quintals, {weather}, {state}\n"
                f"Output:"
            )
            response = client.generate(model=model, prompt=prompt)
            print(response.response)
            return render_template("seller_marketplace.html", user=current_user, roles=current_user.get_role(), response=response.response)
    
    return render_template("seller_marketplace.html", user=current_user, role=current_user.get_role())

@home.route("/logout")
@login_required
@roles_required("seller", "buyer")
def logout():
    session.pop("user_type", None)
    return redirect(url_for('auth.login'))