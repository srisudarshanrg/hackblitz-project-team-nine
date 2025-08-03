import os

from flask import Flask, session
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from .views import home


db = SQLAlchemy()
DB_NAMES = ["database.db"]

session = session

def create_databases(app):
    for db_name in DB_NAMES:
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_name}"
        
        db.init_app(app)
        if not os.path.exists(f'website/{db_name}'):
            with app.app_context():
                db.create_all()
                print("Created Database!")        
            
def register_blueprints(app):
    from .auth import auth
    from .routes import buyer
    
    app.register_blueprint(home, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(buyer, url_prefix="/")

def create_login_manager(app):
    from .models import Buyer, Seller
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        user_type = session.get("user_type")
        if user_type == "buyer":        
            return Buyer.query.get(int(user_id))
        if user_type == "seller":
            return Seller.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "sjkdfj283472983;sfd3{D8D8{{SDLKJ4LK4L4K4L4KL4L4KK44L}"

    create_login_manager(app)
    register_blueprints(app)
    create_databases(app)
    
    return app