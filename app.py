import os
import config
from flask import Flask, render_template, request, redirect, url_for
from models.base_model import db
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from models.user import User
import braintree



login_manager = LoginManager()

web_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instagram_web')
app = Flask('NEXTAGRAM', root_path=web_dir)

csrf = CSRFProtect(app)
login_manager.init_app(app)


if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

@app.before_request
def before_request():
    db.connect()

@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc

# payemnt method
gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=os.getenv("BRAIN_TREE_MERCHANT_ID"),
        public_key=os.getenv("BRAIN_TREE_PUBLIC_KEY"),
        private_key=os.getenv("BRAIN_TREE_PRIVATE_KEY")
    )
)
