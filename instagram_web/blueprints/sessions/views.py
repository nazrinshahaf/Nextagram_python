from flask import Blueprint, render_template,request,url_for,redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import *



sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


@sessions_blueprint.route('/login', methods=['GET'])
def new():
    return render_template('sessions/new.html')
    
@sessions_blueprint.route('/', methods=['POST'])
def create():
    
    username_input = request.form.get('username_input')
    password_input = request.form.get('password_input')

    user_info = user.User.get_or_none(username_input == user.User.username)
    if user_info:
        if check_password_hash(user_info.password, password_input):
            return redirect(url_for('users.index'))
        else:
            flash('Wrong username or password')
            return render_template('sessions/new.html', username_input= username_input, password_input=password_input)
        
    
