from flask import Blueprint, render_template,request,url_for,redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models.payment import *
from flask_wtf.csrf import CSRFProtect
from flask_login import current_user
from app import gateway

payment_blueprint = Blueprint('payment',
                            __name__,
                            template_folder='templates')


@payment_blueprint.route("/payment/<img_id>", methods=["GET"])
def new_payment(img_id):
    client_token = gateway.client_token.generate({})

    return render_template('payment/new.html', client_token = client_token, img_id= img_id)

@payment_blueprint.route("/payment/<img_id>", methods=["POST"])
def payment(img_id):
    nonce = request.form.get("nonce")
    amount = request.form.get("amount")

    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce,
        "options": {
        "submit_for_settlement": True
        }
    })


    if result.is_success:
        new_donation = Payment(user=current_user.id,image=img_id, amount=amount, message="TEST")

        if new_donation.save():
            return redirect(url_for('home'))
        else:
            return render_template('payment/new.html')
    else:
        flash("something went wrong")
        return render_template('payment/new.html')
    
        