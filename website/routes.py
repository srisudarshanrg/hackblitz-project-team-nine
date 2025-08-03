from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .functions import roles_required
from .models import Produce, BuyProduce
from . import db

buyer = Blueprint("buyer", __name__)

@buyer.route("/buyer-marketplace", methods=["GET", "POST"])
@roles_required("buyer")
@login_required
def buyer_marketplace():
    produces = Produce.query.filter_by().all()

    if request.method == "POST":
        if "produce_id" in request.form:
            produce_id = int(request.form.get("produce_id"))
            seller_id = int(request.form.get("seller_id"))
            new_buy_produce = BuyProduce(produce_id=produce_id, seller_id=seller_id, buyer_id=current_user.id)
            db.session.add(new_buy_produce)
            db.session.commit()

            flash(message="Sent interest in buying", category="success")

    return render_template("buyer_marketplace.html", user=current_user, role=current_user.get_role(), produces=produces)