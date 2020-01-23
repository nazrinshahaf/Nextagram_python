from flask import Blueprint, render_template,request,url_for,redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import *
from flask_wtf.csrf import CSRFProtect
from flask_login import login_user,current_user
from instagram_web.util.helpers import *


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
        login_user(new_user)
        return redirect(('/'))
    else:
        for e in new_user.errors:
            flash(e)
        return render_template('users/new.html', email_input=email_input, name_input=name_input,password_input=password_input,username_input=username_input, errors=new_user.errors)


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    return render_template('users/profile.html')
    


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/edit', methods=['GET'])
def edit():
    return render_template('users/edit.html')


@users_blueprint.route('/edit', methods=['POST'])
def update():
    email_edit_input = request.form.get('email_edit_input')
    username_edit_input = request.form.get('username_edit_input')
    # password_edit_input = request.form.get('password_edit_input')
    
    new_info = user.User.update(username= username_edit_input, email=email_edit_input).where(user.User.id == current_user.id)

    new_info.execute()
    return redirect(url_for('home'))
    
@users_blueprint.route('/edit/password', methods=["GET"])
def password():
    return render_template('users/edit_password.html')

@users_blueprint.route('/edit/password', methods=["POST"])
def edit_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    comfirm_password = request.form.get('comfirm_password')
    
    if check_password_hash(current_user.password, current_password):
        if current_password == comfirm_password or current_password == new_password:
            flash("Current password and new password are the same")
            return render_template('users/edit_password.html')
        elif comfirm_password == new_password:
            hashed_password = generate_password_hash(new_password)
            new_info = user.User.update(password = hashed_password).where(user.User.id == current_user.id)
            
            new_info.execute()
            return redirect(url_for('home'))
        else:
            flash('New passsword and comfirm password is not the same')
            return render_template('users/edit_password.html')
    else:
        flash('Wrong password')
        return render_template('users/edit_password.html')
        

@users_blueprint.route('/profile_image', methods=["GET"])
def profile():
    if current_user.is_active:
        return render_template('users/profile_image.html')
    else:
        return redirect(url_for('home'))

@users_blueprint.route('/profile_image', methods=["POST"])
def upload():
    
    if "user_file" not in request.files:
        return "No user_file key in request.files"
    
    file = request.files['user_file']
    if file.filename == "":
        return "Please select a file"

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file,S3_BUCKET)

        profile_image_url = str(output)
        new_image = user.User.update(profile_image = profile_image_url ).where(user.User.id == current_user.id)
        new_image.execute()
        return redirect(url_for('home'))
        
    else:
        return redirect(url_for('home'))

