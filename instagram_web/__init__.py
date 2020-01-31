from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.payment.views import payment_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from app import oauth
from flask_login import current_user
from models import *
from models.followers import *

assets = Environment(app)
assets.register(bundles)
oauth.init_app(app)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint)
app.register_blueprint(payment_blueprint)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route("/")
def home():
    if current_user.is_authenticated:
        allfollowers = [] 
        for f in current_user.followers:
            following = False
            follower_profile = user.User.get_by_id(f.follower)
            if Followers.get_or_none(Followers.follower == current_user.id, Followers.followed == follower_profile.id):
                following = True
            allfollowers.append({
                "profile" : follower_profile,
                "following": following
            })
        return render_template('home.html', allfollowers = allfollowers)
    else:
        return render_template('sessions/new.html')


