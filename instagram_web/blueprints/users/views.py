from flask import Blueprint, render_template,request,url_for,redirect, flash
from werkzeug.security import generate_password_hash
from models import *



users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    name_input = request.form.get('name_input')
    email_input = request.form.get('email_input')
    username_input = request.form.get('username_input')
    password_input = request.form.get('password_input')
    
    new_user = user.User(name=name_input, email=email_input, username=username_input, password=password_input)

    if new_user.save():
        # return redirect(url_for('users.index')) #use when done with signup 
        return redirect(url_for('users.new'))
    else:
        for e in new_user.errors:
            flash(e)
        return render_template('users/new.html', email_input=email_input, name_input=name_input,password_input=password_input,username_input=username_input, errors=new_user.errors)


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass

