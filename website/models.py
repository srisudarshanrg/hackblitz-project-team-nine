from . import db
from flask_login import UserMixin
class Seller(db.Model, UserMixin):
    __tablename__ = "seller"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)

    def get_role(self):
        return "seller"

class Buyer(db.Model, UserMixin):
    __tablename__ = "buyer"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)

    def get_role(self):
        return "buyer"

class Produce(db.Model):
    __tablename__ = "produce"
    
    id = db.Column(db.Integer(), primary_key=True)
    produce_name = db.Column(db.String())    
    seller_id = db.Column(db.Integer(), db.ForeignKey("seller.id"))

class BuyProduce(db.Model):
    __tablename__ = "buyer_produce"

    id = db.Column(db.Integer(), primary_key=True)   
    produce_id = db.Column(db.Integer(), db.ForeignKey("produce.id")) 
    seller_id = db.Column(db.Integer(), db.ForeignKey("produce.id"))
    buyer_id = db.Column(db.Integer(), db.ForeignKey("buyer.id"))