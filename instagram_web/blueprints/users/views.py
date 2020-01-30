import os
from flask import Blueprint, render_template,request,url_for,redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import *
from models.followers import *
from flask_wtf.csrf import CSRFProtect
from flask_login import login_user,current_user
from instagram_web.util.helpers import *
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime




users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


now = datetime.now()
timestamp = datetime.timestamp(now)

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
    # user profile of visited user
    user_profile = user.User.get(user.User.username == username)

    # if current user is logged in
    if current_user.is_authenticated:
        # if visited user exist
        if user.User.get_or_none(username == username):
            # if current user is current user
            if current_user.username == username:
                img = user.User.get_by_id(current_user.id).images
                return render_template('users/my_profile.html', img = img)
            else:
                
                following = ""
                if Followers.get_or_none(Followers.follower == current_user.id, Followers.followed == user_profile.id):
                    following = True
                else:
                    following = False 

                img = user.User.get_by_id(user_profile.id).images
                return render_template('users/profile.html', user_profile= user_profile, img = img, following = following)
        else:
            return render_template('/users/user_doesnt_exist.html')
    else:
        return render_template('/users/not_logged_in.html')
    


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


@users_blueprint.route('/upload_image', methods=["GET"])
def images():
    return render_template('users/upload_image.html')

@users_blueprint.route('/upload_image', methods=["POST"])
def upload_user_images():
    if "user_file" not in request.files:
        return "No user_file key in request.files"
    
    file = request.files['user_file']
    if file.filename == "":
        return "Please select a file"

    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file,S3_BUCKET)
        image_url = str(output)
        image_description = request.form.get('image_description')
        user_images.User_images.create(user=current_user.id,image=image_url,description=image_description)
        
        # delete create later on so u can save and validate
        return redirect(url_for('home'))
        
    else:
        return redirect(url_for('home'))

@users_blueprint.route('/search',methods=["GET"])
def search():
     search_username = request.args.get("search_username")
     return redirect(url_for('users.show', username = search_username))

@users_blueprint.route('/private', methods=["POST"])
def make_private():
    
    x = user.User.update(is_private = not current_user.is_private).where(user.User.id == current_user.id)
    x.execute()
    if current_user.is_private:
        flash("Account set to public")
    else:
        flash("Account set to private")

    
    return redirect(url_for('users.show', username = current_user.username))
    
@users_blueprint.route('/follow/<username>', methods=["POST"])
def follow(username):
    pending = False
    user_profile = user.User.get_or_none(user.User.username == username)

    # if profile exist
    if user_profile:
        # if profile is private
        if user_profile.is_private:
            message = Mail(
                from_email='NazNextagram@gmail.com',
                to_emails="upchuck333@yahoo.com",
                subject="You've received a donation!",
                html_content=render_template("users/follow_request.html", timestamp = timestamp,user_profile = user_profile))
            try:
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(str(e))

            pending = True
            flash("follow request sent")
            return render_template("/users/profile.html", user_profile = user_profile, pending = pending)
        # if profile public
        else:
            following = Followers(follower = current_user.id, followed = user_profile.id).save() 
            return redirect(url_for('users.show', username = username))
    # if user doesnt exist
    else:
        return render_template('/users/user_doesnt_exist.html')
    
@users_blueprint.route(f"/follow/private/<username>/{timestamp}", methods=["GET"])
def follow_request(username):
    user_profile = user.User.get_or_none(user.User.username == username)
    following = Followers(follower = current_user.id, followed = user_profile.id).save() 
    
    return redirect(url_for("home"))

@users_blueprint.route('/unfollow/<username>', methods=["POST"])
def unfollow(username):
    followed_user = user.User.get_or_none(user.User.username == username)
    unfollowed = Followers.get_or_none(Followers.follower == current_user.id, Followers.followed == followed_user.id).delete_instance()
    # if unfollowed:
    #     flash("Unfollowed")
    # else:
    #     flash("Something went wrong")
    return redirect(url_for('home'))



