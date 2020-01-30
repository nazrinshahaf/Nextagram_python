from flask import Blueprint, render_template,request,url_for,redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import *

from flask_wtf.csrf import CSRFProtect
from flask_login import login_user,logout_user
from app import oauth

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


@sessions_blueprint.route('/login', methods=['GET'])
def new():
    return render_template('sessions/new.html')

@sessions_blueprint.route('/destroy', methods=['POST'])
def delete():
    logout_user()
    flash("Succesfully signed out")
    return redirect('/')

@sessions_blueprint.route('/', methods=['POST'])
def create():
    
    username_input = request.form.get('username_input')
    password_input = request.form.get('password_input')
    
    user_info = user.User.get_or_none(username_input == user.User.username)
    if user_info:
        if check_password_hash(user_info.password, password_input):
            login_user(user_info)
            return redirect('')
        else:
            flash('Wrong username or password')
            return render_template('sessions/new.html', username_input= username_input)


@sessions_blueprint.route("/login_with_google", methods=["GET"])
def login_with_google():
    redirect_uri = url_for('sessions.perform_login_with_google', _external = True)
    return oauth.google.authorize_redirect(redirect_uri)

@sessions_blueprint.route("/sessions/authorize/google", methods=["GET"])
def perform_login_with_google():
    token = oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    print("token= ", token)
    print("email= ", email)
    existing_user = user.User.get_or_none(user.User.email == email)
    if existing_user is None:
        flash("You are not signed up")
        return redirect(url_for('users.new'))
    login_user(existing_user)
    return redirect(url_for('home'))

