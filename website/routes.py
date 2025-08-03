from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .functions import roles_required
from .models import Produce, BuyProduce

buyer = Blueprint("buyer", __name__)

@buyer.route("/buyer-marketplace")
@roles_required("buyer")
@login_required
def buyer_marketplace():
    produces = Produce.query.filter_by().all()
    return render_template("buyer_marketplace.html", user=current_user, role=current_user.get_role(), produces=produces, current_user=current_user, role=current_user.get_role())