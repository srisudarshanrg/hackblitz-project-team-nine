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
    from .models import Produce, BuyProduce, Buyer
    from . import db

    sold_produces = Produce.query.filter_by().all()

    interested_buyers = BuyProduce.query.filter_by(seller_id=current_user.id).all()

    final_interested_buyers = []

    for i in interested_buyers:
        produce_name = Produce.query.filter_by(id=i.produce_id).first()
        produce_name = produce_name.produce_name
        buyer_name = Buyer.query.filter_by(id=i.buyer_id).first()
        buyer_name = buyer_name.username
        final_interested_buyers.append({
            "id": i.produce_id,
            "produce_name": produce_name,
            "buyer_name": buyer_name
        })
    
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
            return render_template("seller_marketplace.html", user=current_user, roles=current_user.get_role(), response=response.response, sold_produces=sold_produces)
        elif "add_produce" in request.form:
            produce_name = request.form.get("produce_name")
            quantity = int(request.form.get("quantity"))
            price = int(request.form.get("price"))
            new_produce = Produce(produce_name=produce_name, quantity=quantity, price=price, seller_id=current_user.id)
            db.session.add(new_produce)
            db.session.commit()

        elif "buy_produce_id" in request.form:
            id = int(request.form.get("buy_produce_id"))
            row = BuyProduce.query.filter_by(produce_id=id).all()
            for r in row:
                db.session.delete(r)
                db.session.commit()
    return render_template("seller_marketplace.html", user=current_user, role=current_user.get_role(), interested_buyers=final_interested_buyers)

@home.route("/logout")
@login_required
@roles_required("seller", "buyer")
def logout():
    session.pop("user_type", None)
    return redirect(url_for('auth.login'))