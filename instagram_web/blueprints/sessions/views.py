from flask import Blueprint, render_template,request,url_for,redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import *
from flask_wtf.csrf import CSRFProtect
from flask_login import login_user,logout_user

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
            # return render_template('home.html')
        else:
            flash('Wrong username or password')
            return render_template('sessions/new.html', username_input= username_input)

 