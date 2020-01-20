from flask import Blueprint, render_template
from werkzeug.security import generate_password_hash


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

    hashed_password_input = generate_password_hash(password_input)

    new_user = user.User.create(name=name_input, email=email_input, username=username_input, password=hashed_password_input)
    
    if new_user.save():
        return redirect(url_for('user_sign_up'))
    else:
        return render_template('users/new.html', email_input=email_input, name_input=name_input,password_input=password_input,username_input=username_input)


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


# @app.route("/sign-up-form" ,methods=["POST"])
# def new_user_sign_up():
#     name_input = request.form.get('name_input')
#     email_input = request.form.get('email_input')
#     username_input = request.form.get('username_input')
#     password_input = request.form.get('password_input')

#     hashed_password_input = generate_password_hash(password_input)

#     new_user = user.User.create(name=name_input, email=email_input, username=username_input, password=hashed_password_input)
    
#     if new_user.save():
#         return redirect(url_for('user_sign_up'))
#     else:
#         return render_template('users/new.html', email_input=email_input, name_input=name_input,password_input=password_input,username_input=username_input)